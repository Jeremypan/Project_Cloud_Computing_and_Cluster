import tweepy
from auth import consumer_key,consumer_secret,access_token,access_token_secret
from timelineThread import timelineThread
import json
import couchdb
from dblogin import user, password
import sys

class dbStreamListener(tweepy.StreamListener):
    def __init__(self, api,db):
        self.api = api
        self.db = db
        self.count = 0
 
    def on_data(self, data):
        try:
            tweet = json.loads(data)
        except Exception:
            print("Failed to parse tweet data\n")
            tweet = None
            
        if tweet:
            if "id" in tweet and "text" in tweet and "id_str" in tweet and "user" in tweet:
                self.count += 1
                user = tweet["user"]["screen_name"]
                t = timelineThread(self.count,self.api,user,self.db)
                t.start()
        else:
            print("Received a responce that is not a tweet\n")
            print(tweet)
            
        return True
    
    def on_error(self, status):
        print(status)    

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit = True,wait_on_rate_limit_notify= True)

    # select database
    server = couchdb.Server("http://%s:%s@localhost:5984/" % (user,password))
    dbname = "harvester"
    if dbname in server:
        db = server[dbname]
    else:
        db = server.create(dbname)

    listener = dbStreamListener(api,db)

    stream = tweepy.Stream(auth, listener,tweet_mode="extended")
    stream.filter(locations=[112.6233053121, -44.1178998761, 154.0490928206, -10.6805030025])
