import threading
import tweepy
import json
import couchdb

class timelineThread (threading.Thread):
    def __init__(self, threadID, api, user, db):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.user = user
        self.api = api
        self.db = db
      
    def run(self):
        tweets = self.api.user_timeline(screen_name = self.user,count=100,tweet_mode='extended')
        for tweet in tweets:
            jsonStr = json.dumps(tweet._json)
            jsonObj = json.loads(jsonStr)
            if "id" in jsonObj and "full_text" in jsonObj and "id_str" in jsonObj and "place" in jsonObj:
                try:
                    if jsonObj["place"] is not None:
                        self.db[str(jsonObj["id_str"])] = jsonObj
                        # print(jsonObj["place"]["full_name"])
                except couchdb.http.ResourceConflict:
                    continue
        

    
