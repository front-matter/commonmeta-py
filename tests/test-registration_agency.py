import pytest
import os
import vcr
import json
from requests import HTTPError
from talbot import Crossref

cr = Crossref(mailto = "info@front-matter.io")


@pytest.mark.vcr
def test_registration_agency():
    "registration agency"
    res = cr.registration_agency("10.1126/science.169.3946.635")
    assert list == res.__class__
    assert str == res[0].__class__


@pytest.mark.vcr
def test_registration_agency_unicode():
    "registration agency- unicode"
    res = cr.registration_agency("10.1126/science.169.3946.635")
    assert list == res.__class__
    assert str == res[0].__class__

@pytest.mark.vcr
def test_registration_agency_kisti():
    "registration agency KISTI"
    res = cr.registration_agency("10.5012/bkcs.2013.34.10.2889")
    assert list == res.__class__
    assert str == res[0].__class__

@pytest.mark.vcr
def test_registration_agency_jalc():
    "registration agency JaLC"
    res = cr.registration_agency("10.1241/johokanri.39.979")
    assert list == res.__class__
    assert str == res[0].__class__

@pytest.mark.vcr
def test_registration_agency_medra():
    "registration agency mEDRA"
    res = cr.registration_agency("10.3280/ecag2018-001005")
    assert list == res.__class__
    assert str == res[0].__class__

@pytest.mark.vcr
def test_registration_agency():
    "registration agency OP"
    res = cr.registration_agency("10.2903/j.efsa.2018.5239")
    for dict in res:
        print(dict)
    assert list == res.__class__
    assert str == res[0].__class__

@pytest.mark.vcr
def test_registration_agency_bad_request():
    "registration agency - bad request"
    with pytest.raises(HTTPError):
        cr.registration_agency(5)
