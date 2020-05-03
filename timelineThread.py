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
        counter = 0
        print ("Starting " + str(self.threadID)+" for user %s\n" %self.user)
        tweets = self.api.user_timeline(screen_name = self.user,count=100,tweet_mode='extended')
        for tweet in tweets:
            jsonStr = json.dumps(tweet._json)
            jsonObj = json.loads(jsonStr)
            if "id" in jsonObj and "full_text" in jsonObj and "id_str" in jsonObj:
                jsonObj["doc_type"] = "tweet"
                try:
                    self.db[str(jsonObj["id_str"])] = jsonObj
                    counter += 1
                except couchdb.http.ResourceConflict:
                    continue
        print ("Exiting " + str(self.threadID)+" %d inserted\n" %counter)
        

    
