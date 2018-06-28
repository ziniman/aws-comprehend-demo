#!/usr/local/bin/python2.7

import boto3
import json
import argparse
import feedparser
from time import sleep

# command line arguments
parser = argparse.ArgumentParser(description='Reads RSS feed and parse all items with comprehend')
parser.add_argument('feed', help='RSS feed URL')
parser.add_argument('region', default='us-east-1', nargs='?', help='Comprehend region (default=us-east-1')
args = parser.parse_args()
print(args)

comprehend = boto3.client(service_name='comprehend', region_name=args.region)

feed = feedparser.parse(args.feed)

#print (feed)

for obj in feed.entries:
    title = (obj['title'])
    text = (obj['description'])

    print('Calling DetectSentiment for %s' % title)
    sentiment_response = comprehend.detect_sentiment(Text=title, LanguageCode='en')

    sentiment_score = sentiment_response["SentimentScore"]
    Sentiment= str(sentiment_response['Sentiment'])
    Positive = str(sentiment_score['Positive'])
    Negative = str(sentiment_score['Negative'])
    Neutral = str(sentiment_score['Neutral'])
    Mixed = str(sentiment_score['Mixed'])

    output = ('"%s", P"%s", NG"%s", NT"%s", M"%s"') % (Sentiment, Positive, Negative, Neutral, Mixed)
    print (output)
    print('End of DetectSentiment\n')
    #sleep (5)
