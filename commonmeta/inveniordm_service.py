"""Talk to InvenioRDM through its service layer instead of its REST API.

The reader and writer address an InvenioRDM instance over HTTP with a bearer
token, which is the only option from outside. Code running *inside* an instance
— a Celery task, a CLI command — has a better one: call the services directly as
``system_identity``, which InvenioRDM's ``SystemProcess()`` permission generator
admits.

That is not merely tidier. Over HTTP the instance authenticates to itself, rate
limits itself, and needs a credential to be issued, stored and rotated; and the
credential has to belong to a superuser, because ``Permission`` implicitly
admits ``superuser_access`` and that is the only way a human token satisfies a
policy written as ``[SystemProcess()]``. A machine writing to itself should not
need a human's superuser token.

Nothing here is imported unless the backend is switched on, so commonmeta-py
keeps working with no InvenioRDM installed — the invenio packages are not
dependencies and never become any.

Usage::

    from commonmeta.inveniordm_service import system_process

    with system_process():
        push_inveniordm(metadata, host, token=None)

or, equivalently, through the writer's own switch::

    push_inveniordm(metadata, host, token=None, system_process=True)

The switch lives in a :class:`~contextvars.ContextVar`, so it follows the
``with`` block rather than the process: two Celery tasks in one worker, one
pushing to its own instance and one to a remote one, do not disturb each other.

When the backend is on but unusable — no InvenioRDM installed, or no Flask
application context — :func:`active_backend` returns ``None`` and every call
site falls back to HTTP. That keeps the failure mode "behaves as before" rather
than "raises somewhere deep in a writer".
"""

from __future__ import annotations

import hashlib
import io
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator

from .io_utils import former_pdf_filenames

log = logging.getLogger(__name__)

#: Whether the current context should use the service layer.
_enabled: ContextVar[bool] = ContextVar("commonmeta_inveniordm_system_process")


def is_checksum_of(checksum: str | None, content: bytes) -> bool:
    """Whether a file entry's checksum is the checksum of these bytes.

    The entry names the algorithm it used - `md5:2c4c37ad…` - and it names it
    because the storage backend chose it: invenio-files-rest hashes with md5
    unless a backend overrides `_init_hash`, and no setting changes that. The
    name is read rather than assumed, so an instance that hashes otherwise is
    compared with rather than uploaded to again on every run. An entry with no
    checksum, or one named by an algorithm this Python cannot compute, is not
    a match, and the file is written again.
    """
    algorithm, _, digest = (checksum or "").partition(":")
    if not digest:
        return False
    try:
        message_digest = hashlib.new(algorithm)
    except ValueError:
        log.warning(f"Cannot check a {algorithm} checksum, rewriting the file")
        return False
    message_digest.update(content)
    return message_digest.hexdigest() == digest


@contextmanager
def system_process(enabled: bool = True) -> Iterator[None]:
    """Route InvenioRDM reads and writes through the service layer."""
    token = _enabled.set(enabled)
    try:
        yield
    finally:
        _enabled.reset(token)


def enabled() -> bool:
    """Whether the service layer was asked for in this context."""
    return _enabled.get(False)


def active_backend() -> "ServiceBackend | None":
    """Return the service backend, or ``None`` to fall back to HTTP.

    ``None`` covers three cases that are all "use HTTP": not asked for, no
    InvenioRDM installed, and no application context to serve a request from.
    """
    if not enabled():
        return None
    try:
        from flask import has_app_context

        if not has_app_context():
            log.warning(
                "system_process requested without a Flask application context; "
                "falling back to the REST API"
            )
            return None
        from invenio_access.permissions import system_identity  # noqa: F401
        from invenio_rdm_records.proxies import current_rdm_records  # noqa: F401
    except ImportError:
        log.warning(
            "system_process requested but InvenioRDM is not installed; "
            "falling back to the REST API"
        )
        return None
    return ServiceBackend()


def reason(error: Exception) -> str:
    """What a service exception says, which `str()` alone does not always tell.

    InvenioRDM's validation errors carry their detail in ``messages`` and
    stringify to nothing, so logging ``str(e)`` for one wrote "Error
    publishing draft record: " and left the record's actual problem - a doi
    the pid component rejected, say - out of the log entirely.
    """
    messages = getattr(error, "messages", None)
    if messages:
        return f"{type(error).__name__}: {messages}"
    return str(error) or type(error).__name__


#: Whether this process has already said that files cannot be modified.
_locked_bucket_reported = False


def report_failed_attachment(record_id: str, key: str, detail: str) -> None:
    """Log a refused file, saying once what a locked bucket would take to fix.

    An instance that does not allow a published record's files to be modified
    refuses every one of them, so a run over a few hundred posts reports the
    same fact a few hundred times. It is worth saying — those records will not
    get a rendition until the setting changes — but worth saying once, and
    with the setting named. Everything else is logged as it happens.
    """
    global _locked_bucket_reported

    message = f"Could not attach {key} to record {record_id}: {detail}"
    if "bucket is locked" not in detail.lower():
        log.warning(message, extra={"record_id": record_id})
        return
    if _locked_bucket_reported:
        log.debug(message, extra={"record_id": record_id})
        return
    _locked_bucket_reported = True
    log.warning(
        f"{message} A published record takes a file where InvenioRDM 14 is "
        "configured for it: RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED, with a "
        "policy that admits this caller. Reported once per process.",
        extra={"record_id": record_id},
    )


class ServiceBackend:
    """The operations the reader and writer need, as service calls.

    Each method mirrors the REST helper it stands in for, including the status
    strings it writes onto ``record``: callers switch transport without learning
    a second vocabulary for what happened.

    Errors are logged and turned into the same ``error_*`` statuses the HTTP
    path uses. A service call raising where the REST call would have returned a
    4xx should not abort an import run.
    """

    # -- plumbing ---------------------------------------------------------

    @property
    def _identity(self):
        from invenio_access.permissions import system_identity

        return system_identity

    @property
    def _records(self):
        from invenio_rdm_records.proxies import current_rdm_records

        return current_rdm_records.records_service

    @property
    def _communities(self):
        from invenio_communities.proxies import current_communities

        return current_communities.service

    @property
    def _record_communities(self):
        from invenio_rdm_records.proxies import current_record_communities_service

        return current_record_communities_service

    # -- reads ------------------------------------------------------------

    def read_record(self, record_id: str) -> dict | None:
        """Read a published record."""
        try:
            return self._records.read(self._identity, record_id).to_dict()
        except Exception as e:
            log.error(f"Error reading record {record_id}: {reason(e)}", exc_info=True)
            return None

    def search_records(self, query: str) -> dict | None:
        """Search published records, returning the REST-shaped envelope."""
        try:
            return self._records.search(
                self._identity, params={"q": query, "size": 1}
            ).to_dict()
        except Exception as e:
            log.error(f"Error searching records: {reason(e)}", exc_info=True)
            return None

    def search_community_by_slug(
        self, slug: str, type: str | None = None
    ) -> str | None:
        """Return a community id for a slug, of this type or a subject area.

        The type is what keeps a subject from filing a post under someone
        else's blog. Slugs are unique across every kind of community, so a post
        subject that slugifies to `crossref` matches the Crossref blog as
        readily as a topic, and the record joins it -- silently, and for good,
        since nothing ever removes a community from a record. The REST path
        this stands in for has always narrowed the search the same way, by
        sending `type` twice: the type asked for, and `subject`.

        Left unset the search spans every community, which is what the callers
        that mean a blog want.
        """
        query = f"slug:{slug}"
        if type:
            query += f" AND (metadata.type.id:{type} OR metadata.type.id:subject)"
        try:
            results = self._communities.search(
                self._identity, params={"q": query, "size": 1}
            ).to_dict()
        except Exception as e:
            log.error(f"Error searching for community: {reason(e)}", exc_info=True)
            return None
        hits = ((results or {}).get("hits") or {}).get("hits") or []
        return hits[0].get("id") if hits else None

    def get_record_communities(self, record: dict) -> list | None:
        """Return the communities a record belongs to, as REST returns them.

        The REST path returns ``hits.hits`` — community objects — and the caller
        reads ``c.get("id")`` from each. ``parent.communities.ids`` is a list of
        plain id strings, so it is wrapped rather than returned as it comes:
        handing back strings raised ``'str' object has no attribute 'get'`` in
        add_record_to_communities, and every record in the batch was recorded
        with status "error" after having been published.
        """
        data = self.read_record(record.get("id"))
        if data is None:
            return None
        ids = ((data.get("parent") or {}).get("communities") or {}).get("ids") or []
        return [{"id": community_id} for community_id in ids]

    # -- writes -----------------------------------------------------------

    def create_draft_record(self, record: dict, output: dict) -> dict:
        """Create a new draft."""
        try:
            item = self._records.create(self._identity, output)
        except Exception as e:
            log.error(f"Error creating draft record: {reason(e)}", exc_info=True)
            record["status"] = "error_draft"
            return record
        data = item.to_dict()
        record["id"] = data.get("id")
        record["created"] = data.get("created")
        record["updated"] = data.get("updated")
        record["status"] = "draft"
        return record

    def update_draft_record(self, record: dict, inveniordm_data: dict) -> dict:
        """Update a draft."""
        try:
            item = self._records.update_draft(
                self._identity, record["id"], data=inveniordm_data
            )
        except Exception as e:
            log.error(f"Error updating draft record: {reason(e)}", exc_info=True)
            record["status"] = "error_update_draft_record"
            return record
        record["updated"] = item.to_dict().get("updated")
        record["status"] = "updated"
        return record

    def publish_draft_record(self, record: dict) -> dict:
        """Publish a draft, discarding one that can never be published.

        A draft whose files are turned off while the record behind it has one
        fails with "403 Forbidden: Files are not enabled", and fails the same
        way on every later run, since each one opens that same draft. Where
        that is what publish says, the draft goes and the published record
        stands as it was - the recoverable outcome, and the only one that ends
        without a record that can never be written again.
        """
        try:
            item = self._records.publish(self._identity, record["id"])
        except Exception as e:
            detail = reason(e)
            if "files are not enabled" in detail.lower():
                discarded = self._discard_draft(
                    record,
                    "its files are turned off while the record behind it has one, "
                    "which publish cannot reconcile",
                )
                if discarded.get("status") == "draft_discarded":
                    return discarded
            log.error(f"Error publishing draft record: {detail}", exc_info=True)
            record["status"] = "error_publish_draft_record"
            return record
        data = item.to_dict()
        record["created"] = data.get("created")
        record["updated"] = data.get("updated")
        record["status"] = "published"
        return record

    def edit_published_record(self, record: dict) -> dict:
        """Open a draft on a published record."""
        try:
            item = self._records.edit(self._identity, record["id"])
        except Exception as e:
            log.error(
                f"Error creating draft from published record: {reason(e)}",
                exc_info=True,
            )
            record["status"] = "error_edit_published_record"
            return record
        record["updated"] = item.to_dict().get("updated")
        record["status"] = "edited"
        return record

    def create_new_version(self, record: dict) -> dict:
        """Create a new version of a published record."""
        try:
            item = self._records.new_version(self._identity, record["id"])
        except Exception as e:
            log.error(f"Error creating new version: {reason(e)}", exc_info=True)
            record["status"] = "error_create_new_version"
            return record
        data = item.to_dict()
        record["id"] = data.get("id")
        record["updated"] = data.get("updated")
        record["status"] = "new_version"
        return record

    def reserve_doi(self, record: dict) -> dict:
        """Reserve a DOI on a draft."""
        try:
            item = self._records.pids.create(self._identity, record["id"], "doi")
        except Exception as e:
            log.error(
                f"Error reserving DOI for record {record.get('id')}: {reason(e)}",
                exc_info=True,
            )
            record["status"] = "error_reserve_doi"
            return record
        doi = ((item.to_dict().get("pids") or {}).get("doi") or {}).get("identifier")
        record["doi"] = doi
        record["status"] = "doi_reserved"
        return record

    def _file_entry(self, record_id: str, key: str) -> dict:
        """A draft file's entry, empty when the draft carries no such file."""
        try:
            return self._records.draft_files.read_file_metadata(
                self._identity, record_id, key
            ).to_dict()
        except Exception:
            return {}

    def _drop_file(self, record_id: str, key: str) -> bool:
        """Remove a draft file entry. Returns whether it is gone."""
        try:
            self._records.draft_files.delete_file(self._identity, record_id, key)
            return True
        except Exception as e:
            log.warning(
                f"Could not remove file {key} from record {record_id}: {reason(e)}",
                extra={"record_id": record_id},
            )
            return False

    def _list_files(self, record_id: str) -> list[dict]:
        """Every entry on the draft, none where the listing is refused."""
        try:
            listing = self._records.draft_files.list_files(
                self._identity, record_id
            ).to_dict()
        except Exception as e:
            log.warning(
                f"Could not list the files of record {record_id}: {reason(e)}",
                extra={"record_id": record_id},
            )
            return []
        return listing.get("entries") or []

    def draft_file_keys(self, record_id: str) -> list[str]:
        """Every key on the draft whose transfer completed.

        What the draft has to publish, which is asked before it is turned
        metadata-only: a file that is there — an older rendition left in place,
        one this run could not replace — is one the publish would keep and
        disabling files would strip.
        """
        return [
            entry.get("key")
            for entry in self._list_files(record_id)
            if entry.get("status") == "completed" and entry.get("key")
        ]

    def _incomplete_keys(self, record_id: str) -> list[str]:
        """Every key on the draft whose transfer never completed.

        Publish walks all of a draft's entries and refuses the lot if any one
        of them is incomplete, so what blocks a record is not necessarily the
        file this run is attaching. A draft was found carrying two abandoned
        entries under keys the run had never heard of — the rendition's name
        comes from the doi, and this record's doi had changed between runs, so
        each attempt registered a new key and left the last one behind.
        Answering only for the key in hand meant none of them was ever cleared.
        """
        return [
            entry.get("key")
            for entry in self._list_files(record_id)
            if entry.get("status") != "completed" and entry.get("key")
        ]

    def _enable_files(self, record_id: str) -> bool:
        """Turn files on for a draft, returning whether they are on.

        A record published metadata-only carries ``files.enabled`` false, and
        its draft inherits it. Every file call then refuses with "403
        Forbidden: Files are not enabled", including the one that would remove
        what could not be attached, so the draft is discarded and the record
        stays as it was. The next run edits it again and does the same, which
        is why a record that was once metadata-only never gained a rendition.

        The mirror of _mark_metadata_only: that one turns files off for a draft
        that has none left, this one turns them on for a draft about to be
        given one.
        """
        try:
            draft = self._records.read_draft(self._identity, record_id).to_dict()
            if (draft.get("files") or {}).get("enabled"):
                return True
            draft.setdefault("files", {})["enabled"] = True
            self._records.update_draft(self._identity, record_id, data=draft)
            return True
        except Exception as e:
            log.warning(
                f"Could not enable files on record {record_id}: {reason(e)}",
                extra={"record_id": record_id},
            )
            return False

    def _mark_metadata_only(self, record_id: str) -> None:
        """Turn files off on a draft that has none left.

        Publishing checks two things, and fixing one exposes the other: a draft
        with files enabled and no entries is rejected with "Missing uploaded
        files. To disable files for this record please mark it as
        metadata-only." So a draft that lost its only file has to say it is
        metadata-only, or it is no more publishable than before.

        Only ever called when no entries remain, and only where no published
        record carries one either. An edit of a published record usually
        carries that record's files, but not where this run dropped them to
        write them again and then could not: the draft is empty and the record
        is not, and publishing that edit copies the draft's `enabled` onto the
        record, clears the record's own entries with it, and then syncs through
        the manager it has just turned off:

            InvalidOperationError: 403 Forbidden: Files are not enabled.

        The record is then unpublishable until its draft is discarded, having
        been turned metadata-only over a pdf it still had.
        """
        try:
            files = self._records.draft_files.list_files(
                self._identity, record_id
            ).to_dict()
            if files.get("entries") or self._published_file_keys(record_id):
                return
            draft = self._records.read_draft(self._identity, record_id).to_dict()
            draft.setdefault("files", {})["enabled"] = False
            self._records.update_draft(self._identity, record_id, data=draft)
        except Exception as e:
            log.warning(
                f"Could not mark record {record_id} as metadata-only: {reason(e)}",
                extra={"record_id": record_id},
            )

    def upload_file(self, record: dict, key: str, content: bytes) -> dict:
        """Attach a file to a draft: register the key, send bytes, commit.

        Re-runnable, which the three calls alone are not. ``init_files`` refuses
        a key the draft already carries, and a draft can carry one from an
        attempt that registered the key and then failed before committing. That
        entry never completes, so the 400 repeats on every later run and
        ``publish`` rejects the draft for good:

            400 Bad Request: File with key <key> already exists.
            ValidationError: One or more files have not completed their
            transfer, please wait.

        A key that is already there and holds these very bytes is left alone.
        One that holds different bytes is replaced, so that a post edited after
        publication gets the rendition of what it says now: InvenioRDM 14 lets
        a published record's files be modified without a new version, where
        RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED is on and a policy admits the
        caller. Where it is not, the bucket is locked, the file cannot be
        dropped, and the one already attached stays.

        Failure leaves no incomplete entry behind, because that is what blocks
        the publish. Returning without the file is a valid outcome, which the
        caller publishes anyway; returning with a half-registered one is not.
        Where such an entry cannot be removed, the draft is discarded rather
        than left to fail its publish for good - see `_abandon_draft`.
        """
        files = self._records.draft_files
        identity, record_id = self._identity, record["id"]

        # Clear anything that would make the publish fail, under any key: one
        # incomplete entry refuses the whole draft, and it is not necessarily
        # the file being attached here. Where one cannot be removed — a locked
        # bucket — the draft is beyond saving on this run, so it is discarded
        # and the next run gets a clean one.
        for stale in self._incomplete_keys(record_id):
            if not self._drop_file(record_id, stale):
                return self._abandon_draft(record, stale)

        # The rendition of this post that a run before the rename attached is
        # the same rendition under an older name, and nothing else would ever
        # look for it: left alone, the record would carry two pdfs of one post
        # and deposit both. Where the bucket refuses the removal the old one
        # stays and the new one is written beside it, which is the tolerance a
        # changed file gets too - a record with a rendition beats none.
        for superseded in former_pdf_filenames(key):
            if self._file_entry(record_id, superseded):
                self._drop_file(record_id, superseded)

        # Whatever is left under this key is complete, the incomplete ones
        # having just gone.
        entry = self._file_entry(record_id, key)
        if entry.get("status") == "completed":
            if is_checksum_of(entry.get("checksum"), content):
                record["files"] = [key]
                return record
            if not self._drop_file(record_id, key):
                # A locked bucket, most likely. The attached file is the older
                # rendition of the same post, which beats no file at all.
                record["files"] = [key]
                return record

        if not self._enable_files(record_id):
            # Every file call refuses while they are off, including the one
            # that would clean up after a failed attach, so there is nothing to
            # gain by trying and a draft to lose by leaving an entry behind.
            return record

        try:
            files.init_files(identity, record_id, [{"key": key}])
            # The length is passed rather than left to the storage backend to
            # work out from the stream. The bytes are already in memory, so it
            # costs nothing, and a backend that cannot size a stream itself has
            # no other way to know: S3 in particular needs the length up front.
            files.set_file_content(
                identity,
                record_id,
                key,
                io.BytesIO(content),
                content_length=len(content),
            )
            files.commit_file(identity, record_id, key)
        except Exception as e:
            report_failed_attachment(record_id, key, reason(e))
            return self._discard_incomplete(record, key)

        # Asked rather than assumed. All three calls can return without raising
        # and still leave the entry with no object version behind it, which is
        # the state publish refuses — and the silent version of it is the worse
        # one, since nothing in the log says the rendition did not arrive.
        if self._file_entry(record_id, key).get("status") != "completed":
            report_failed_attachment(
                record_id, key, "the transfer did not complete, and did not say so"
            )
            return self._discard_incomplete(record, key)

        record["files"] = [key]
        return record

    def _discard_incomplete(self, record: dict, key: str) -> dict:
        """Leave nothing behind that would make the draft unpublishable."""
        record_id = record["id"]
        if self._file_entry(record_id, key).get("status") == "completed":
            record["files"] = [key]
            return record
        if not self._drop_file(record_id, key):
            return self._abandon_draft(record, key)
        self._mark_metadata_only(record_id)
        return record

    def _abandon_draft(self, record: dict, key: str) -> dict:
        """Discard a draft that carries a file it can never publish.

        A file entry whose transfer never completed makes publish refuse the
        draft - "One or more files have not completed their transfer, please
        wait" - and where the instance does not allow a published record's
        files to be modified, that entry cannot be removed either. The record
        then fails on this run and on every run after it, since each one opens
        the same draft and finds the same entry.
        """
        return self._discard_draft(
            record,
            f"it carries {key} with an incomplete transfer, which cannot be "
            "removed and which publish refuses",
        )

    def _discard_draft(self, record: dict, why: str) -> dict:
        """Discard a draft that can never publish, keeping the record it edits.

        Discarding undoes this run's edit and leaves the published record as it
        was, which is the recoverable outcome: what publish refuses lives in
        the draft, so the next run opens a clean one. Only ever done where
        there is a published record to fall back on - a draft that has never
        been published is left alone, since discarding that would delete the
        record - and it tells the caller not to publish what is no longer
        there.
        """
        record_id = record["id"]
        if not self._is_published(record_id):
            return record
        try:
            self._records.delete_draft(self._identity, record_id)
        except Exception as e:
            log.error(
                f"Could not discard the draft of record {record_id}: {reason(e)}",
                extra={"record_id": record_id},
            )
            return record
        log.warning(
            f"Discarded the draft of record {record_id}: {why}. The published "
            "record is unchanged, and the next run edits it again.",
            extra={"record_id": record_id},
        )
        record["status"] = "draft_discarded"
        return record

    def _published_file_keys(self, record_id: str) -> list[str]:
        """The files of the published record a draft was opened on, by key.

        Not `read_record`, which logs a missing record as an error: a draft
        with nothing published behind it is an ordinary answer here, and the
        common one.
        """
        try:
            published = self._records.read(self._identity, record_id).to_dict()
        except Exception:
            return []
        return list((published.get("files") or {}).get("entries") or [])

    def _is_published(self, record_id: str) -> bool:
        """Whether a published record stands behind this draft.

        Not `read_record`, which logs a missing record as an error: here it is
        an ordinary answer, and the common one for a draft being created.
        """
        try:
            self._records.read(self._identity, record_id)
            return True
        except Exception:
            return False

    def add_record_to_community(self, record: dict, community_id: str) -> dict:
        """Add a record to a community."""
        try:
            self._record_communities.add(
                self._identity,
                record["id"],
                {"communities": [{"id": community_id}]},
            )
        except Exception as e:
            # The REST path treats "already a member" and a logo-less community
            # as warnings rather than failures; so does this.
            log.warning(
                "Failed to add record to community: %s",
                reason(e),
                extra={"record_id": record.get("id"), "community_id": community_id},
            )
        return record
