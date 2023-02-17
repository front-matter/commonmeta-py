# -*- coding: utf-8 -*-

# talbot

"""
talbot library
~~~~~~~~~~~~~~~~~~~~~

talbot is a low level client for the Crossref search API.

Usage::

   from talbot import Crossref
   cr = Crossref()

   # setup a different base URL
   Crossref(base_url = "http://some.other.url")

   # setup an api key
   Crossref(api_key = "123456")

   # Make request against works route
   cr.works(ids = '10.1371/journal.pone.0033693')

   # curl options
   ## verbose curl output
   ### setup first
   import requests
   import logging
   import http.client
   http.client.HTTPConnection.debuglevel = 1
   logging.basicConfig()
   logging.getLogger().setLevel(logging.DEBUG)
   requests_log = logging.getLogger("requests.packages.urllib3")
   requests_log.setLevel(logging.DEBUG)
   requests_log.propagate = True
   ### then make request
   cr.works(query = "ecology")
"""

__title__ = "talbot"
__version__ = "0.5.1"
__author__ = "Martin Fenner"
__license__ = "MIT"

from .metadata import Metadata
