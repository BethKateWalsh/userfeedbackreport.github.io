#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from twitter_api import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

#import modules
from pymongo import MongoClient
import tweepy

# Connect to Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


#Get 1000 tweets
searchQuery = "@azuresupport"
searched_tweets = []
last_id = -1
max_tweets = 1000

while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=searchQuery, count=100, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

        for tweet in searched_tweets:
            # Fields from the user object
            id_user = tweet.user.id
            id_str_user = tweet.user.id_str
            name_user = tweet.user.name
            screen_name_user = tweet.user.screen_name
            location_user = tweet.user.location
            description_user = tweet.user.description
            url_user = tweet.user.url
            followers_count_user_user = tweet.user.followers_count
            favourites_count_user = tweet.user.favourites_count
            lang_user = tweet.user.lang
            # Fields from the status object
            id_status = tweet.id
            id_str_status = tweet.id_str
            textstatus = tweet.text
            created_at_status = tweet.created_at
            truncated = tweet.truncated
            in_reply_to_screen_name = tweet.in_reply_to_screen_name
            retweet_count = tweet.retweet_count
            favorite_count = tweet.favorite_count
            retweeted = tweet.retweeted
            lang_status = tweet.lang
            print(tweet.text.encode('utf-8'))