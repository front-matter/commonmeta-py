Talbot uses `pytest` and `vcrpy` for testing. To run the tests, issue one of the following commands from the root folder:

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
