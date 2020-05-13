import tweepy
from auth import consumer_key,consumer_secret,access_token,access_token_secret
import json
import couchdb
from dblogin import user, password
import sys

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit = True,wait_on_rate_limit_notify= True)

place_id = "3f14ce28dc7c4566"

server = couchdb.Server("http://%s:%s@localhost:5984/" % (user,password))
dbname = "harvester"
if dbname in server:
    db = server[dbname]
else:
    db = server.create(dbname)

while True:
    tweets = api.search(q="place:%s" % place_id,count=100,tweet_mode="extended")
    for tweet in tweets:
        jsonStr = json.dumps(tweet._json)
        jsonObj = json.loads(jsonStr)
        if "id" in jsonObj and "full_text" in jsonObj and "id_str" in jsonObj and "place" in jsonObj:
            try:
                db[str(jsonObj["id_str"])] = jsonObj
                # print(jsonObj["place"]["full_name"])
            except couchdb.http.ResourceConflict:
                continue
            
