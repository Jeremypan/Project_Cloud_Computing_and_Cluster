import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import logging
import json
import time
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
        self.api=tweepy.API(auth)
        self.max_tweets=50
        
    def on_data(self, raw_data):
        try:  
            # self.file.write(json.dumps(raw_data+"\n",ensure_ascii=False))
            self.tweet_count_stream+=1
            # logging.info("{0}, {1}".format(self.tweet_count_stream,raw_data))
            
            data=json.loads(raw_data)
            """
            Raw Data

             ['created_at', 'id', 'id_str', 'text', 'source', 'truncated', 
            'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 
            'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors', 
            'retweeted_status', 'is_quote_status', 'quote_count', 'reply_count', 
            'retweet_count', 'favorite_count', 'entities', 'favorited', 'retweeted', 'filter_level', 'lang', 'timestamp_ms']
            """
            user_detail=data['user']

            """
            user data detail
            ['id', 'id_str', 'name', 'screen_name', 'location', 'url', 'description', 'translator_type', 'protected', 
            'verified', 'followers_count', 'friends_count', 'listed_count', 'favourites_count', 'statuses_count', 
            'created_at', 'utc_offset', 'time_zone', 'geo_enabled', 'lang', 
            'contributors_enabled', 'is_translator', 'profile_background_color', 'profile_background_image_url', 
            'profile_background_image_url_https', 'profile_background_tile', 'profile_link_color', 'profile_sidebar_border_color', 
            'profile_sidebar_fill_color', 'profile_text_color', 'profile_use_background_image', 'profile_image_url', 'profile_image_url_https', 
            'profile_banner_url', 'default_profile', 'default_profile_image', 'following', 'follow_request_sent', 'notifications']
            """
            print("id: "+ str(data['id']))
            # print("user_location: {0}".format(user_detail['location']))
            # print("time_zone: {0}".format(user_detail['time_zone']))
            # print("geo: {0}".format(data['geo']))
            # print("coordiante: {0}".format(data['coordinates']))
            # print("place: {0}".format(data['place']))
            min_longitude=data['place']['bounding_box']['coordinates'][0][0][0]
            max_longitude=data['place']['bounding_box']['coordinates'][0][1][0]
            min_latitude=data['place']['bounding_box']['coordinates'][0][0][1]
            max_latitude=data['place']['bounding_box']['coordinates'][0][2][1]
            geocode="{0},{1},100km".format(((max_latitude-min_latitude)/2)+min_latitude,((max_longitude-min_longitude)/2)+min_longitude)
            print("geocode: {0}".format(geocode))
            time.sleep(1)
            #radius search the tweet from stream 
            searched_tweets = self.api.search(geocode=geocode,count=self.max_tweets)
            print("Num of Radius Search: {0}".format(len(searched_tweets)))
            print("")
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
    twitter_stream.filter(locations=[113.338953078, -43.6345972634, 153.569469029, -10.6681857235])
    # twitter_stream.file.close()