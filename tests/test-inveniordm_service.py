"""Test writing to InvenioRDM through its service layer instead of its API."""

import pytest

from commonmeta import inveniordm_service
from commonmeta.inveniordm_service import active_backend, enabled, system_process
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


class FakeDraftFiles:
    """A draft's files, with the states InvenioRDM actually puts them in."""

    def __init__(self, entries=None, fail_on=None):
        # {key: "completed" | "pending"}
        self.entries = dict(entries or {})
        self.fail_on = fail_on or set()
        self.calls = []

    def read_file_metadata(self, identity, id_, key):
        if key not in self.entries:
            raise KeyError(f"no file {key}")
        return FakeItem({"key": key, "status": self.entries[key]})

    def list_files(self, identity, id_):
        return FakeItem(
            {"entries": [{"key": k, "status": v} for k, v in self.entries.items()]}
        )

    def delete_file(self, identity, id_, key):
        self.calls.append(("delete_file", key))
        self.entries.pop(key, None)

    def init_files(self, identity, id_, data):
        key = data[0]["key"]
        self.calls.append(("init_files", key))
        if key in self.entries:
            # What InvenioRDM raises, and what production hit every run.
            raise Exception(f"400 Bad Request: File with key {key} already exists.")
        if "init" in self.fail_on:
            raise Exception("init blew up")
        self.entries[key] = "pending"

    def set_file_content(self, identity, id_, key, stream):
        self.calls.append(("set_file_content", key))
        if "content" in self.fail_on:
            raise Exception("upload blew up")

    def commit_file(self, identity, id_, key):
        self.calls.append(("commit_file", key))
        if "commit" in self.fail_on:
            raise Exception("commit blew up")
        self.entries[key] = "completed"


class FakeRecordsWithFiles(FakeRecordsService):
    """Records service exposing draft files and a draft to update."""

    def __init__(self, draft_files=None, draft=None):
        super().__init__()
        self.files = draft_files or FakeDraftFiles()
        self.draft = draft if draft is not None else {"files": {"enabled": True}}

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
    files = FakeDraftFiles(entries={"post.pdf": "completed"})
    backend = use_fake_backend(FakeBackend(records=FakeRecordsWithFiles(files)))

    record = backend.upload_file({"id": "abc12-xyz34"}, "post.pdf", b"%PDF-")

    assert record["file"] == "post.pdf"
    assert files.calls == []  # no delete, no re-upload


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
