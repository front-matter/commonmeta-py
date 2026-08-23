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
