from __future__ import absolute_import, print_function

import tweepy
from tweepy import OAuthHandler, Stream, StreamListener

from auth import consumer_key,consumer_secret,access_token,access_token_secret

import json

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit = True,wait_on_rate_limit_notify= True)

#先运行此段代码，结果是全球所有叫Melboune的城市的代码
places = api.geo_search(query="Melbourne", granularity="city")
for place in places:    
    print("placeid:%s" % place)
    

#找到澳大利亚的墨尔本的代码，然后运行此段
"""    
place_id = '01864a8a64df9dc4'
tweets = api.search(q="place:%s" % place_id)

for tweet in tweets:
    print(tweet._json['user']['location'])
"""
