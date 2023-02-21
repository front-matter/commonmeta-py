[![Build](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml/badge.svg)](https://github.com/front-matter/commonmeta-py/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/commonmeta-py.svg)](https://badge.fury.io/py/commonmeta-py)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=front-matter_commonmeta-py&metric=coverage)](https://sonarcloud.io/summary/new_code?id=front-matter_commonmeta-py)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=front-matter_commonmeta-py&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=front-matter_commonmeta-py)
![GitHub](https://img.shields.io/github/license/front-matter/commonmeta-py?logo=MIT)

commonmeta-py is a Python library to implement Commonmeta, the common Metadata Model for Scholarly Metadata. Use commonmeta-py to convert scholarly metadata, in a variety of formats, listed below. Commonmeta-py is work in progress, the first release on PyPi (version 0.5.0) was on February 16, 2023. Up until version 0.5.1, the library was called commonmeta-py. Commonmeta-py is modelled after the [briard ruby gem](https://github.com/front-matter/briard).


## Installation

Stable version
```
pip (or pip3) install commonmeta-py
```

Dev version
```
pip install git+https://github.com/front-matter/commonmeta-py.git#egg=commonmeta-py
```

## Testing

commonmeta-py uses `pytest` and `vcrpy` for testing. To run the tests, issue one of the following commands from the root folder:

All tests:
```
pytest
```

All tests in a test file, e.g. `tests/test-utils.py`:
```
pytest tests/test-utils.py
```

Run a specific test e.g. `test_datacite_api_url` in `tests/test-utils.py`:
```
pytest tests/test-utils.py -k 'test_datacite_api_url'
```

`vcrpy`records HTTP requests to speed up testing. 
