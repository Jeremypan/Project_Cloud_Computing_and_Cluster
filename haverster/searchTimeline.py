from __future__ import absolute_import, print_function

import tweepy

from tweepy import OAuthHandler

# from auth import consumer_key,consumer_secret,access_token,access_token_secret

from timelineThread import timelineThread

import json

import couchdb

from dblogin import user, password

import sys
consumer_key="x4YMdEwhO5T7gzp8wyoPOSRzA"
consumer_secret="yLDAKyghTdUDxlK0x6NXeuyIBXPBpj6uHd0nvLnL4UJmcZLZGf"
access_token="1253888897722925056-yCYIwGQtf2TZ6I8i6dnEfYGEsIzUgZ"
access_token_secret="IU32uJX5nCZ3pE0vbqkl7nDGvjYO7vAXgfnJMmBiGtAgV"



class dbTwitterSearch():
    def __init__ (self,api,db=None):
        self.api=api
        self.db=db
        self.count=0
        self.max_tweets=100

    def twitter_search(self,country):
        places=self.api.geo_search(query=str(country),granularity="country")
        if len(places)==1:
            place_id=places[0].id
        else:
            print("error: more than one country {0}".format(places))
            return
        tweet_batch_num=1
        while True:
            searched_tweets = api.search(q="place:{0}".format(place_id, count=self.max_tweets))
            start_index=0
            print("{0}: Num of tweets: {1}".format(tweet_batch_num,len(searched_tweets)))
            for i in searched_tweets:
                tweet=i._json
                if tweet:
                    print(tweet)
                    if "id" in tweet and "text" in tweet and "id_str" in tweet:
                        self.count += 1
                        user = tweet["user"]["screen_name"]
                        """
                            timeline search
                        """
                        # t = timelineThread(self.count,self.api,user,self.db)
                        # t.start()
                        try:
                            print("%s: %s\n" % (tweet["user"]["screen_name"], tweet["full_text"]))
                        except Exception:
                            print("%s: %s\n" % (tweet["user"]["screen_name"], tweet["text"]))
                else:
                    print("Received a responce that is not a tweet\n")
                    print(tweet)
            if self.count>=10:
                print("finish\n")
                sys.exit(0) 

if __name__ == "__main__":

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    searcher=dbTwitterSearch(api)
    searcher.twitter_search("Australia")
