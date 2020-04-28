import tweepy
consumer_key="x4YMdEwhO5T7gzp8wyoPOSRzA"
consumer_secret="yLDAKyghTdUDxlK0x6NXeuyIBXPBpj6uHd0nvLnL4UJmcZLZGf"
access_token="1253888897722925056-ivRmKkAvi7dx4EKtLeCHyfco0JN8ul"
access_token_secret="RSndyuU04Xqg7VUJLKYslRp72lPI4VAI1JIJacMNfdPOd"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

# user = api.get_user('hjpan1')
# print(user.screen_name)
# print(user.followers_count)
# for friend in user.friends():
#    print(friend.screen_name)



