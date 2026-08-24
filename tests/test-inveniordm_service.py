"""Test writing to InvenioRDM through its service layer instead of its API."""

import logging
from hashlib import md5

import pytest

from commonmeta import inveniordm_service
from commonmeta.inveniordm_service import (
    active_backend,
    enabled,
    reason,
    system_process,
)
from commonmeta.writers.inveniordm_writer import (
    create_draft_record,
    publish_draft_record,
    search_by_slug,
)


class FakeItem:
    """Stands in for a service result, which answers to_dict()."""

    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return self._data


class FakeRecordsService:
    """Records the calls made, so a test can assert the identity used."""

    def __init__(self):
        self.calls = []

    def create(self, identity, data):
        self.calls.append(("create", identity, data))
        return FakeItem({"id": "abc12-xyz34", "created": "now", "updated": "now"})

    def publish(self, identity, id_):
        self.calls.append(("publish", identity, id_))
        return FakeItem({"created": "now", "updated": "later"})


class FakeBackend(inveniordm_service.ServiceBackend):
    """The real backend with the invenio lookups replaced."""

    def __init__(self, records=None, communities_hits=None):
        self.records = records or FakeRecordsService()
        self.communities_hits = communities_hits or []

    @property
    def _identity(self):
        return "system_identity"

    @property
    def _records(self):
        return self.records

    @property
    def _communities(self):
        hits = self.communities_hits

        class _Communities:
            def search(self, identity, params):
                return FakeItem({"hits": {"hits": hits, "total": len(hits)}})

        return _Communities()


@pytest.fixture
def use_fake_backend(monkeypatch):
    """Switch the writer onto a backend that needs no InvenioRDM."""

    def _use(backend):
        monkeypatch.setattr(
            inveniordm_service, "active_backend", lambda: backend, raising=True
        )
        for module in (
            "commonmeta.writers.inveniordm_writer",
            "commonmeta.readers.inveniordm_reader",
        ):
            monkeypatch.setattr(
                f"{module}.active_backend", lambda: backend, raising=True
            )
        return backend

    return _use


def test_the_switch_is_off_by_default():
    """Existing callers keep talking HTTP without changing anything."""
    assert enabled() is False
    assert active_backend() is None


def test_the_switch_only_covers_its_block():
    with system_process():
        assert enabled() is True
    assert enabled() is False


def test_no_backend_without_an_application_context():
    """Asked for but unusable falls back to HTTP rather than raising.

    A worker outside an app context, or a machine with no InvenioRDM installed,
    gets the previous behaviour instead of an exception from inside a writer.
    """
    with system_process():
        assert active_backend() is None


def test_draft_is_created_through_the_service_as_system_identity(use_fake_backend):
    backend = use_fake_backend(FakeBackend())

    record = create_draft_record({}, "example.org", "unused-token", {"title": "A post"})

    assert record["id"] == "abc12-xyz34"
    assert record["status"] == "draft"
    method, identity, data = backend.records.calls[0]
    assert (method, identity) == ("create", "system_identity")
    assert data == {"title": "A post"}


def test_publish_reports_the_same_status_as_the_rest_path(use_fake_backend):
    """Callers read record["status"]; the transport must not change its words."""
    backend = use_fake_backend(FakeBackend())

    record = publish_draft_record({"id": "abc12-xyz34"}, "example.org", None)

    assert record["status"] == "published"
    assert record["updated"] == "later"
    assert ("publish", "system_identity", "abc12-xyz34") in backend.records.calls


def test_community_lookup_by_slug(use_fake_backend):
    use_fake_backend(FakeBackend(communities_hits=[{"id": "comm-1"}]))

    assert search_by_slug("a-blog", "blog", "example.org", None) == "comm-1"


def test_community_lookup_with_no_match(use_fake_backend):
    use_fake_backend(FakeBackend(communities_hits=[]))

    assert search_by_slug("nope", "blog", "example.org", None) is None


def test_a_failing_service_call_becomes_a_status_not_an_exception(use_fake_backend):
    """One bad record must not abort an import run, as with the REST path."""

    class Exploding(FakeRecordsService):
        def create(self, identity, data):
            raise RuntimeError("validation failed")

    use_fake_backend(FakeBackend(records=Exploding()))

    record = create_draft_record({}, "example.org", None, {"title": "A post"})

    assert record["status"] == "error_draft"


# ---------------------------------------------------------------------------
# Regressions from the first production run of the service-layer path
# ---------------------------------------------------------------------------


def file_checksum(content: bytes) -> str:
    """A file's checksum, in the form InvenioRDM reports it."""
    return f"md5:{md5(content).hexdigest()}"


class FakeDraftFiles:
    """A draft's files, with the states InvenioRDM actually puts them in."""

    def __init__(self, entries=None, fail_on=None, checksums=None, locked=False):
        # {key: "completed" | "pending"}
        self.entries = dict(entries or {})
        # {key: bytes the entry holds}, which InvenioRDM reports as an md5
        self.checksums = {k: file_checksum(v) for k, v in (checksums or {}).items()}
        self.fail_on = fail_on or set()
        # a published record whose instance does not allow file modification
        self.locked = locked
        self.calls = []

    def read_file_metadata(self, identity, id_, key):
        if key not in self.entries:
            raise KeyError(f"no file {key}")
        return FakeItem(
            {
                "key": key,
                "status": self.entries[key],
                "checksum": self.checksums.get(key),
            }
        )

    def list_files(self, identity, id_):
        return FakeItem(
            {"entries": [{"key": k, "status": v} for k, v in self.entries.items()]}
        )

    def delete_file(self, identity, id_, key):
        self.calls.append(("delete_file", key))
        if self.locked:
            raise Exception("403 Forbidden: Bucket is locked for modifications.")
        self.entries.pop(key, None)
        self.checksums.pop(key, None)

    def init_files(self, identity, id_, data):
        key = data[0]["key"]
        self.calls.append(("init_files", key))
        if key in self.entries:
            # What InvenioRDM raises, and what production hit every run.
            raise Exception(f"400 Bad Request: File with key {key} already exists.")
        if "init" in self.fail_on:
            raise Exception("init blew up")
        self.entries[key] = "pending"

    def set_file_content(self, identity, id_, key, stream, content_length=None):
        self.calls.append(("set_file_content", key, content_length))
        if "content" in self.fail_on:
            raise Exception("upload blew up")
        self.checksums[key] = file_checksum(stream.read())

    def commit_file(self, identity, id_, key):
        self.calls.append(("commit_file", key))
        if "commit" in self.fail_on:
            raise Exception("commit blew up")
        if "silent" in self.fail_on:
            # Returns cleanly and leaves the entry pending, which is how the
            # 1,235 stuck drafts in production came to be.
            return
        self.entries[key] = "completed"


class FakeRecordsWithFiles(FakeRecordsService):
    """Records service exposing draft files and a draft to update."""

    def __init__(self, draft_files=None, draft=None, published=True):
        super().__init__()
        self.files = draft_files or FakeDraftFiles()
        self.draft = draft if draft is not None else {"files": {"enabled": True}}
        # whether a published record stands behind the draft
        self.published = published

    def read(self, identity, id_):
        if not self.published:
            raise KeyError(f"no published record {id_}")
        return FakeItem({"id": id_})

    def delete_draft(self, identity, id_):
        self.calls.append(("delete_draft", identity, id_))
        self.draft = None

    @property
    def draft_files(self):
        return self.files

    def read_draft(self, identity, id_):
        return FakeItem(dict(self.draft))

    def update_draft(self, identity, id_, data):
        self.draft = data
        self.calls.append(("update_draft", identity, data))
        return FakeItem({"updated": "later"})


def test_communities_are_returned_in_the_shape_the_caller_expects(use_fake_backend):
    """parent.communities.ids is a list of strings; the caller wants objects.

    Returning the strings raised "'str' object has no attribute 'get'" in
    add_record_to_communities, after the record had already been published.
    """
    backend = use_fake_backend(FakeBackend())
    backend.records.read = lambda identity, id_: FakeItem(
        {"parent": {"communities": {"ids": ["comm-1", "comm-2"]}}}
    )

    communities = backend.get_record_communities({"id": "abc12-xyz34"})

    assert communities == [{"id": "comm-1"}, {"id": "comm-2"}]
    assert [c.get("id") for c in communities] == ["comm-1", "comm-2"]


def test_a_stale_pending_file_is_replaced_rather_than_colliding(use_fake_backend):
    """The trap that made a record permanently unpublishable.

    An attempt that registered the key and died before committing leaves a
    pending entry. init_files then refuses the key on every later run, and
    publish refuses the draft because that entry never completes.
    """
    files = FakeDraftFiles(entries={"post.pdf": "pending"})
    backend = use_fake_backend(FakeBackend(records=FakeRecordsWithFiles(files)))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert record["file"] == "post.pdf"
    assert files.entries["post.pdf"] == "completed"
    assert ("delete_file", "post.pdf") in files.calls


def test_an_already_completed_file_is_left_alone(use_fake_backend):
    """The same bytes are already attached, so there is nothing to write."""
    files = FakeDraftFiles(
        entries={"post.pdf": "completed"}, checksums={"post.pdf": b"%PDF-"}
    )
    backend = use_fake_backend(FakeBackend(records=FakeRecordsWithFiles(files)))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert record["file"] == "post.pdf"
    assert files.calls == []  # no delete, no re-upload


def test_a_changed_file_is_replaced(use_fake_backend):
    """A post edited after publication gets the rendition of what it says now.

    InvenioRDM 14 allows a published record's files to be modified without a
    new version, where the instance enables it.
    """
    files = FakeDraftFiles(
        entries={"post.pdf": "completed"}, checksums={"post.pdf": b"%PDF- old"}
    )
    backend = use_fake_backend(FakeBackend(records=FakeRecordsWithFiles(files)))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF- new")

    assert record["file"] == "post.pdf"
    assert files.calls == [
        ("delete_file", "post.pdf"),
        ("init_files", "post.pdf"),
        ("set_file_content", "post.pdf", len(b"%PDF- new")),
        ("commit_file", "post.pdf"),
    ]
    assert files.checksums["post.pdf"] == file_checksum(b"%PDF- new")


def test_a_changed_file_keeps_the_old_one_when_the_bucket_is_locked(use_fake_backend):
    """Without file modification, the rendition already attached stays.

    An older rendition of the same post beats no file at all, and the record
    is published either way.
    """
    files = FakeDraftFiles(
        entries={"post.pdf": "completed"},
        checksums={"post.pdf": b"%PDF- old"},
        locked=True,
    )
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF- new")

    assert record["file"] == "post.pdf"
    assert files.entries == {"post.pdf": "completed"}
    assert files.checksums["post.pdf"] == file_checksum(b"%PDF- old")
    assert ("init_files", "post.pdf") not in files.calls
    assert records.draft["files"]["enabled"] is True


def test_a_failed_upload_leaves_a_publishable_draft(use_fake_backend):
    """Failure must not leave the two states that block publishing.

    An incomplete entry fails the transfer check, and no entry at all fails the
    "Missing uploaded files" check while files are still enabled. So the entry
    is removed and the draft is marked metadata-only.
    """
    files = FakeDraftFiles(fail_on={"commit"})
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert "file" not in record
    assert files.entries == {}
    assert records.draft["files"]["enabled"] is False


def test_files_stay_enabled_when_others_remain(use_fake_backend):
    """An edit of a published record carries its files; do not strip them."""
    files = FakeDraftFiles(entries={"other.pdf": "completed"}, fail_on={"commit"})
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert "other.pdf" in files.entries
    assert records.draft["files"]["enabled"] is True


def test_a_validation_error_says_what_was_invalid(use_fake_backend, caplog):
    """Invenio's validation errors stringify to nothing.

    Publishing a record whose doi the pid component rejects logged "Error
    publishing draft record: " and nothing more, which says only that
    something went wrong.
    """

    class ValidationErrorWithMessageAsList(Exception):
        """What invenio_rdm_records raises, in the shape that matters here."""

        def __init__(self, message):
            super().__init__()
            self.messages = message

    class Rejecting(FakeRecordsService):
        def publish(self, identity, id_):
            raise ValidationErrorWithMessageAsList(
                [{"field": "pids.doi", "messages": ["Invalid DOI for the prefix."]}]
            )

    use_fake_backend(FakeBackend(records=Rejecting()))

    with caplog.at_level(logging.ERROR, logger="commonmeta.inveniordm_service"):
        record = publish_draft_record({"id": "abc12-xyz34"}, "example.org", None)

    assert record["status"] == "error_publish_draft_record"
    logged = caplog.records[0].getMessage()
    assert "ValidationErrorWithMessageAsList" in logged
    assert "Invalid DOI for the prefix." in logged


def test_reason_falls_back_to_the_exception_itself():
    """Anything that does say something keeps saying it."""
    assert reason(RuntimeError("boom")) == "boom"
    assert reason(RuntimeError()) == "RuntimeError"


@pytest.fixture
def unreported_locked_bucket(monkeypatch):
    """Each test starts as a fresh process would, having said nothing yet."""
    monkeypatch.setattr(inveniordm_service, "_locked_bucket_reported", False)


def test_a_locked_bucket_is_reported_once(unreported_locked_bucket, caplog):
    """An instance that refuses every file should not say so for every record."""
    locked = "403 Forbidden: Bucket is locked for modifications."

    with caplog.at_level(logging.DEBUG, logger="commonmeta.inveniordm_service"):
        inveniordm_service.report_failed_attachment("aaa11-bbb22", "a.pdf", locked)
        inveniordm_service.report_failed_attachment("ccc33-ddd44", "b.pdf", locked)

    first, second = caplog.records
    assert first.levelname == "WARNING"
    # named, so that whoever reads it knows what would change the outcome
    assert "RDM_IMMEDIATE_FILE_MODIFICATION_ENABLED" in first.getMessage()
    assert second.levelname == "DEBUG"
    assert "b.pdf" in second.getMessage()


def test_other_refusals_are_reported_every_time(unreported_locked_bucket, caplog):
    """Only the instance-wide state is throttled; a one-off is not."""
    with caplog.at_level(logging.DEBUG, logger="commonmeta.inveniordm_service"):
        inveniordm_service.report_failed_attachment("aaa11-bbb22", "a.pdf", "boom")
        inveniordm_service.report_failed_attachment("ccc33-ddd44", "b.pdf", "boom")

    assert [record.levelname for record in caplog.records] == ["WARNING", "WARNING"]


def test_a_draft_that_can_never_publish_is_discarded(use_fake_backend, caplog):
    """The state that made records fail their publish on every single run.

    A file entry left pending by an earlier attempt cannot be removed while
    the bucket is locked, and publish refuses a draft that carries one.
    """
    files = FakeDraftFiles(entries={"post.pdf": "pending"}, locked=True)
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    with caplog.at_level(logging.WARNING, logger="commonmeta.inveniordm_service"):
        record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert record["status"] == "draft_discarded"
    assert ("delete_draft", "system_identity", "abc12-xyz34") in records.calls
    assert "Discarded the draft" in caplog.records[-1].getMessage()


def test_a_draft_with_nothing_published_behind_it_is_kept(use_fake_backend):
    """Discarding a first draft would delete the record, not undo an edit."""
    files = FakeDraftFiles(entries={"post.pdf": "pending"}, locked=True)
    records = FakeRecordsWithFiles(files, published=False)
    backend = use_fake_backend(FakeBackend(records=records))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert record.get("status") is None
    assert not [call for call in records.calls if call[0] == "delete_draft"]


def test_the_upload_says_how_many_bytes_it_is_sending(use_fake_backend):
    """A storage backend that cannot size a stream has no other way to know.

    Left to work it out, S3 accepted the call, raised nothing, and left the
    entry with no object version behind it.
    """
    files = FakeDraftFiles()
    backend = use_fake_backend(FakeBackend(records=FakeRecordsWithFiles(files)))
    content = b"%PDF-1.7 and some bytes"

    backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", content)

    sent = [c for c in files.calls if c[0] == "set_file_content"]
    assert sent == [("set_file_content", "post.pdf", len(content))]


def test_an_upload_that_fails_silently_is_caught(use_fake_backend):
    """The three calls can all return cleanly and still not attach the file.

    That is the state publish refuses, and the one that left no trace in the
    log: the record simply never gained a rendition. So the entry is asked for
    its status rather than assumed to be good.
    """
    files = FakeDraftFiles(fail_on={"silent"})
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert "file" not in record
    assert files.entries == {}, "the incomplete entry must not survive"
    assert records.draft["files"]["enabled"] is False


def test_stale_entries_under_other_keys_are_cleared(use_fake_backend):
    """What blocks a publish need not be the file this run is attaching.

    Draft 9ch1z-brd41 carried two abandoned entries, rqawv-7g546.pdf and
    3ty7x-g7a23.pdf, while the run was attaching j63pf-38v68.pdf: the
    rendition's name comes from the doi, and that record's doi had changed
    between runs. Asking only about the key in hand found nothing to clean, so
    publish kept refusing the draft over files the run never mentioned.
    """
    files = FakeDraftFiles(
        entries={"rqawv-7g546.pdf": "pending", "3ty7x-g7a23.pdf": "pending"}
    )
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    record = backend.upload_file({"id": "9ch1z-brd41"}, "j63pf-38v68.pdf", b"%PDF-")

    assert record["file"] == "j63pf-38v68.pdf"
    assert set(files.entries) == {"j63pf-38v68.pdf"}, "the strays must be gone"
    assert files.entries["j63pf-38v68.pdf"] == "completed"


def test_a_stray_that_cannot_be_dropped_abandons_the_draft(use_fake_backend):
    """A locked bucket keeps the stray, so the draft can never publish.

    Discarding it leaves the published record untouched and lets the next run
    open a clean draft, which is the only way out that does not lose the
    record.
    """
    files = FakeDraftFiles(entries={"rqawv-7g546.pdf": "pending"}, locked=True)
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    record = backend.upload_file({"id": "9ch1z-brd41"}, "j63pf-38v68.pdf", b"%PDF-")

    assert record.get("status") == "draft_discarded"
    assert "file" not in record


def test_a_completed_file_of_another_name_is_left_alone(use_fake_backend):
    """Only incomplete entries block a publish; complete ones are the record."""
    files = FakeDraftFiles(
        entries={"figure.png": "completed"}, checksums={"figure.png": b"PNG"}
    )
    records = FakeRecordsWithFiles(files)
    backend = use_fake_backend(FakeBackend(records=records))

    backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert files.entries["figure.png"] == "completed"
    assert files.entries["post.pdf"] == "completed"


def test_the_pdf_is_named_after_the_record_not_the_run():
    """Two dois are in play, and only one of them lasts.

    Rogue Scholar mints a random suffix for a post that has none, on every read
    of the feed, while the record is matched by guid — so metadata.id is a
    different doi each run for the same post. Naming the file from it left one
    record holding three entries, each named after a doi that existed only for
    the length of the run that made it.
    """
    from commonmeta.writers.inveniordm_writer import pdf_filename

    class Meta:
        id = "https://doi.org/10.59350/j63pf-38v68"  # minted this run

    # The record's own doi, which upsert_record adopts and the update leaves
    # alone, names the file.
    assert (
        pdf_filename(Meta(), {"doi": "https://doi.org/10.59350/rqawv-7g546"})
        == "rqawv-7g546.pdf"
    )
    # A bare doi is accepted as readily as a url.
    assert pdf_filename(Meta(), {"doi": "10.59350/rqawv-7g546"}) == "rqawv-7g546.pdf"
    # A genuinely new post has no record to take a doi from, so the one in hand
    # is the one it will keep.
    assert pdf_filename(Meta(), None) == "j63pf-38v68.pdf"
    assert pdf_filename(Meta(), {}) == "j63pf-38v68.pdf"
