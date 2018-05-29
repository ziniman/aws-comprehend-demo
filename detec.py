#!/usr/local/bin/python2.7

import boto3
import json
import argparse

# command line arguments
parser = argparse.ArgumentParser(description='Read files from a S3 bucket and parse all of them with comprehend')
parser.add_argument('bucket', help='S3 bucket name')
parser.add_argument('output_folder', default='comprehend', nargs='?', help='Comprehend output folder')
parser.add_argument('delimiter', default=',', nargs='?', help='Delimiter for csv records (default=,)')
parser.add_argument('region', default='us-east-1', nargs='?', help='Comprehend region (default=us-east-1')
args = parser.parse_args()
print(args)

s3 = boto3.resource('s3')
bucket = s3.Bucket(args.bucket)

comprehend = boto3.client(service_name='comprehend', region_name=args.region)

# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.
for obj in bucket.objects.all():
    key = obj.key
    body = obj.get()['Body'].read()
    text = body
    print('Calling DetectSentiment for ###%s###' % text)
    sentiment_response = comprehend.detect_sentiment(Text=text, LanguageCode='en')

    sentiment_score = sentiment_response["SentimentScore"]
    Sentiment= str(sentiment_response['Sentiment'])
    Positive = str(sentiment_score['Positive'])
    Negative = str(sentiment_score['Negative'])
    Neutral = str(sentiment_score['Neutral'])
    Mixed = str(sentiment_score['Mixed'])

    output = ('"%s", "%s", "%s", "%s", "%s", "%s"') % (text, Sentiment, Positive, Negative, Neutral, Mixed)
    print (output)
    object = s3.Object(args.bucket, '%s/%s.csv' % (args.output_folder, key))
    object.put(Body=output)

    print('End of DetectSentiment\n')
