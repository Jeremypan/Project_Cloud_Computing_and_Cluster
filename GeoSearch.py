from __future__ import absolute_import, print_function

import tweepy

from auth import consumer_key,consumer_secret,access_token,access_token_secret

from timelineThread import timelineThread

import json

import couchdb

from dblogin import user, password

import sys


class dbTwitterSearch(placeid):





places=api.geo_search(query="Australia", granularity="country")
for place in places:
    print("placeid:%s" % place)