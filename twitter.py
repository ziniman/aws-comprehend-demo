#!/usr/local/bin/python2.7

import tweepy
import argparse
import boto3
import secrets

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# command line arguments
parser = argparse.ArgumentParser(description='Read twitts for specific tag and parse all of them with comprehend')
parser.add_argument('tag', help='Tag to search')
parser.add_argument('count', default='10', nargs='?', help='How many items to retrive.')
parser.add_argument('region', default='us-east-1', nargs='?', help='Comprehend region (default=us-east-1')
args = parser.parse_args()
# print(args)

auth = tweepy.OAuthHandler(secrets.api_key, secrets.api_secret)
auth.set_access_token(secrets.access_token, secrets.access_secret)
api = tweepy.API(auth)

tweets = api.search(q=args.tag, count = args.count)
comprehend = boto3.client(service_name='comprehend', region_name=args.region)

posts = []
timestamp = []
locations = []
sentiments = []
positive = []
negative = []
neutral = []
colors = {'POSITIVE': bcolors.GREEN, 'NEGATIVE': bcolors.RED, 'MIXED': bcolors.BLUE}

for i in range(len(tweets)):
    d = tweets[i].text
    ts = tweets[i].created_at
    l = tweets[i].user.location

    if d != '':
        res = comprehend.detect_sentiment(Text=d, LanguageCode='en')
        s = res.get('Sentiment')
        p = res.get('SentimentScore')['Positive']
        neg = res.get('SentimentScore')['Negative']
        neu = res.get('SentimentScore')['Neutral']
        color = colors.get(s, bcolors.ENDC)

    timestamp.append(ts)
    posts.append(d)
    locations.append(l)
    #sentiments.append(s)
    #positive.append(p)
    #negative.append(neg)
    #neutral.append(neu)

    print (color + '*********\nData: %s\nTwitt: %s\nSentiment: %s\n') % (ts, d, s)
