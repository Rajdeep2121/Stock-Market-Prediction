import tweepy
import csv
import json
import json

# create a dictionary to store your twitter credentials

twitter_cred = dict()

# Enter your own consumer_key, consumer_secret, access_key and access_secret
# Replacing the stars ("********")

twitter_cred['CONSUMER_KEY'] = ''
twitter_cred['CONSUMER_SECRET'] = ''
twitter_cred['ACCESS_KEY'] = ''
twitter_cred['ACCESS_SECRET'] = ''


# Save the information to a json so that it can be reused in code without exposing
# the secret info to public

with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)
with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    all_the_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    all_the_tweets.extend(new_tweets)
    oldest_tweet = all_the_tweets[-1].id - 1
   
    while len(new_tweets):
        new_tweets = api.user_timeline(screen_name=screen_name,count=200, max_id=oldest_tweet)
        all_the_tweets.extend(new_tweets)
        oldest_tweet = all_the_tweets[-1].id - 1
        print ('...%s tweets have been downloaded so far' % len(all_the_tweets))
        outtweets = [[tweet.id_str, tweet.created_at,
        tweet.text.encode('utf-8')] for tweet in all_the_tweets]
   
    with open(screen_name + '_tweets.csv', 'w', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(outtweets)

if __name__ == '__main__':
    get_all_tweets(input("Enter the twitter handle of the person whose tweets you want to download:- "))