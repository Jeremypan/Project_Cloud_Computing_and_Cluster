import tweepy
import time
# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)

API_KEY="x4YMdEwhO5T7gzp8wyoPOSRzA"
API_SECRET="yLDAKyghTdUDxlK0x6NXeuyIBXPBpj6uHd0nvLnL4UJmcZLZGf"
ACCESS_TOKEN="1253888897722925056-yCYIwGQtf2TZ6I8i6dnEfYGEsIzUgZ"
ACCESS_TOKEN_SECRET="IU32uJX5nCZ3pE0vbqkl7nDGvjYO7vAXgfnJMmBiGtAgV"




auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# query = 'geocode='
max_tweets = 100
tweet_batch_num=1
locations=[113.338953078, -43.6345972634, 153.569469029, -10.6681857235]
geocode=[(locations[2]-locations[0])//2+locations[0],(locations[3]-locations[1])//2+locations[1],1242.742] #2000km radius
print(geocode)
while True:
    time.sleep(1)
    searched_tweets = api.search(q="place:%s"%'3f14ce28dc7c4566',count=max_tweets)
    start_index=0
    print("{0}: Num of tweets: {1}".format(tweet_batch_num,len(searched_tweets)))
    while start_index<len(searched_tweets):
        """
        data keys:

        ['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'metadata', 'source', 'in_reply_to_status_id', 
        'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 
        'user', 'geo', 'coordinates', 'place', 'contributors', 'retweeted_status', 
        'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'lang']

        """
        data=searched_tweets[start_index]._json
        available_num_with_location=0     
        # if data['geo']!=None or data['coordinates']!=None:
        #     available_num_with_location+=1
        #     print(data['place'])
        if data ['place'] is not None:
            min_longitude=data['place']['bounding_box']['coordinates'][0][0][0]
            max_longitude=data['place']['bounding_box']['coordinates'][0][1][0]
            min_latitude=data['place']['bounding_box']['coordinates'][0][0][1]
            max_latitude=data['place']['bounding_box']['coordinates'][0][2][1]
            print([min_longitude,min_latitude,max_longitude,max_latitude])
            if min_longitude>=locations[0] and max_longitude<=locations[2] and min_latitude>=locations[1] and max_latitude<=locations[3]:
                print(data)
        start_index+=1
    tweet_batch_num+=1