import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import logging
import json
# from config import Config

consumer_key="x4YMdEwhO5T7gzp8wyoPOSRzA"
consumer_secret="yLDAKyghTdUDxlK0x6NXeuyIBXPBpj6uHd0nvLnL4UJmcZLZGf"
access_token="1253888897722925056-yCYIwGQtf2TZ6I8i6dnEfYGEsIzUgZ"
access_token_secret="IU32uJX5nCZ3pE0vbqkl7nDGvjYO7vAXgfnJMmBiGtAgV"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


#Stream_API
class MyListener(StreamListener):
    def __init__(self):
        self.tweet_count_stream=1
        self.file=open('python.txt',"w")
    def on_data(self, raw_data):
        try:  
            self.file.write(json.dumps(raw_data+"\n",ensure_ascii=False))
            self.tweet_count_stream+=1
            # logging.info("{0}, {1}".format(self.tweet_count_stream,raw_data))
            print("{0}, {1}".format(self.tweet_count_stream,raw_data))
            return True
        except BaseException as e:
            print("Error on_data:%s" % str(e))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            logging.error("Error {0} Rate limit reached".format(status_code))
        logging.error("Error {0}".format(status_code))
        

    def on_timeout(self):
        logging.warning("ERROR: Timeout...")
        return True

if __name__ == "__main__":
    twitter_stream = Stream(auth, MyListener())
    track_content=['COVID-19','covid-19','covid19','CONVID19','convid','CONVID','Covid-19','Covid19','Coronavirus','CORONAVIRUS','coronavirus']
    twitter_stream.filter(track=track_content,locations=[113.338953078, -43.6345972634, 153.569469029, -10.6681857235],languages=['en'])
    twitter_stream.file.close()