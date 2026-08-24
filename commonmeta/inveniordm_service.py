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

import io
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator

log = logging.getLogger(__name__)

#: Whether the current context should use the service layer.
_enabled: ContextVar[bool] = ContextVar("commonmeta_inveniordm_system_process")


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
            log.error(f"Error reading record {record_id}: {str(e)}", exc_info=True)
            return None

    def search_records(self, query: str) -> dict | None:
        """Search published records, returning the REST-shaped envelope."""
        try:
            return self._records.search(
                self._identity, params={"q": query, "size": 1}
            ).to_dict()
        except Exception as e:
            log.error(f"Error searching records: {str(e)}", exc_info=True)
            return None

    def search_community_by_slug(self, slug: str) -> str | None:
        """Return a community id for a slug."""
        try:
            results = self._communities.search(
                self._identity, params={"q": f"slug:{slug}", "size": 1}
            ).to_dict()
        except Exception as e:
            log.error(f"Error searching for community: {str(e)}", exc_info=True)
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
            log.error(f"Error creating draft record: {str(e)}", exc_info=True)
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
            log.error(f"Error updating draft record: {str(e)}", exc_info=True)
            record["status"] = "error_update_draft_record"
            return record
        record["updated"] = item.to_dict().get("updated")
        record["status"] = "updated"
        return record

    def publish_draft_record(self, record: dict) -> dict:
        """Publish a draft."""
        try:
            item = self._records.publish(self._identity, record["id"])
        except Exception as e:
            log.error(f"Error publishing draft record: {str(e)}", exc_info=True)
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
                f"Error creating draft from published record: {str(e)}", exc_info=True
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
            log.error(f"Error creating new version: {str(e)}", exc_info=True)
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
                f"Error reserving DOI for record {record.get('id')}: {str(e)}",
                exc_info=True,
            )
            record["status"] = "error_reserve_doi"
            return record
        doi = ((item.to_dict().get("pids") or {}).get("doi") or {}).get("identifier")
        record["doi"] = doi
        record["status"] = "doi_reserved"
        return record

    def _file_status(self, record_id: str, key: str) -> str | None:
        """Return a draft file's transfer status, or None when it has none."""
        try:
            entry = self._records.draft_files.read_file_metadata(
                self._identity, record_id, key
            ).to_dict()
        except Exception:
            return None
        return entry.get("status")

    def _drop_file(self, record_id: str, key: str) -> bool:
        """Remove a draft file entry. Returns whether it is gone."""
        try:
            self._records.draft_files.delete_file(self._identity, record_id, key)
            return True
        except Exception as e:
            log.warning(
                f"Could not remove file {key} from record {record_id}: {str(e)}",
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

        Only ever called when no entries remain, which keeps it away from the
        case that matters: an edit of a published record carries that record's
        files, and disabling files there would strip them on publish.
        """
        try:
            files = self._records.draft_files.list_files(
                self._identity, record_id
            ).to_dict()
            if files.get("entries"):
                return
            draft = self._records.read_draft(self._identity, record_id).to_dict()
            draft.setdefault("files", {})["enabled"] = False
            self._records.update_draft(self._identity, record_id, data=draft)
        except Exception as e:
            log.warning(
                f"Could not mark record {record_id} as metadata-only: {str(e)}",
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

        A key that is already there and completed is left alone — the file is
        attached, which is all the caller wanted. An incomplete one is dropped
        and re-uploaded.

        Failure leaves no incomplete entry behind, because that is what blocks
        the publish. Returning without the file is the intended outcome (the
        draft of a published record has its files locked, and the REST path logs
        and publishes anyway); returning with a half-registered one is not.
        """
        files = self._records.draft_files
        identity, record_id = self._identity, record["id"]

        status = self._file_status(record_id, key)
        if status == "completed":
            record["file"] = key
            return record
        if status is not None and not self._drop_file(record_id, key):
            # It could not be removed, so it will block the publish whatever
            # happens next. Nothing to gain by uploading over it.
            return record

        try:
            files.init_files(identity, record_id, [{"key": key}])
            files.set_file_content(identity, record_id, key, io.BytesIO(content))
            files.commit_file(identity, record_id, key)
        except Exception as e:
            log.warning(
                f"Could not attach {key} to record {record_id}: {str(e)}",
                extra={"record_id": record_id},
            )
            if self._file_status(record_id, key) != "completed":
                self._drop_file(record_id, key)
                self._mark_metadata_only(record_id)
            return record
        record["file"] = key
        return record

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
                str(e),
                extra={"record_id": record.get("id"), "community_id": community_id},
            )
        return record
