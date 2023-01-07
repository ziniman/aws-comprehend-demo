#!/usr/local/bin/python3.9

#Reads a RSS feed and look for sentiment in title
#Options feeds for demo
#https://www.reddit.com/r/aws/.rss
#https://stackoverflow.com/feeds/tag?tagnames=amazon-web-services&sort=newest
#http://rss.cnn.com/rss/edition_world.rss

import boto3
import json
import argparse
import feedparser
from time import sleep

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

# command line arguments
parser = argparse.ArgumentParser(description='Reads RSS feed and parse all items with comprehend')
parser.add_argument('feed', help='RSS feed URL')
parser.add_argument('region', default='us-east-1', nargs='?', help='Comprehend region (default=us-east-1')
args = parser.parse_args()
#print(args)

comprehend = boto3.client(service_name='comprehend', region_name=args.region)

feed = feedparser.parse(args.feed)

#print (feed)

for obj in feed.entries:
    title = (obj['title'])
    #text = (obj['description'])

    if title:
        print('Calling DetectSentiment for "%s"' % title)
        sentiment_response = comprehend.detect_sentiment(Text=title, LanguageCode='en')
        phrases_response = comprehend.detect_key_phrases(Text=title, LanguageCode='en')

        sentiment_score = sentiment_response["SentimentScore"]
        Sentiment= str(sentiment_response['Sentiment'])
        Positive = str(sentiment_score['Positive'])
        Negative = str(sentiment_score['Negative'])
        Neutral = str(sentiment_score['Neutral'])
        Mixed = str(sentiment_score['Mixed'])

        key_phrases = phrases_response['KeyPhrases']

        colors = {'POSITIVE': bcolors.GREEN, 'NEGATIVE': bcolors.RED, 'MIXED': bcolors.BLUE}
        color = colors.get(Sentiment, bcolors.ENDC)

        if key_phrases:
            print (bcolors.YELLOW + 'Key Phrases:')
            for word in key_phrases:
                print (word['Text'])

        output = (color + '"%s", P"%s", NG"%s", NT"%s", M"%s"' + bcolors.ENDC) % (Sentiment, Positive, Negative, Neutral, Mixed)

        print (output)
        print('**********************\n')
        #sleep (2)
