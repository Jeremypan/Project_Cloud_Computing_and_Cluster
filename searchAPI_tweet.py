import tweepy
# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)

API_KEY="x4YMdEwhO5T7gzp8wyoPOSRzA"
API_SECRET="yLDAKyghTdUDxlK0x6NXeuyIBXPBpj6uHd0nvLnL4UJmcZLZGf"
ACCESS_TOKEN="1253888897722925056-yCYIwGQtf2TZ6I8i6dnEfYGEsIzUgZ"
ACCESS_TOKEN_SECRET="IU32uJX5nCZ3pE0vbqkl7nDGvjYO7vAXgfnJMmBiGtAgV"




auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

query = 'covid'
max_tweets = 100
searched_tweets = api.search(q=query,count=max_tweets)
for i in searched_tweets:
    print(i._json)