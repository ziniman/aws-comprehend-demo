#!/usr/local/bin/python3.9

import boto3
import json
import argparse
import csv

s3 = boto3.resource('s3')

# command line arguments
parser = argparse.ArgumentParser(description='Read files from a S3 bucket and parse all of them with comprehend')
parser.add_argument('bucket', help='S3 bucket name')
parser.add_argument('input_file', help='Input file')
parser.add_argument('delimiter', default='\t', nargs='?', help='Delimiter for csv records (default=TAB)')
parser.add_argument('region', default='us-east-1', nargs='?', help='Comprehend region (default=us-east-1')
args = parser.parse_args()
print(args)

bucket = args.bucket

with open(args.input_file) as csv_file:
    tokens = csv.reader(csv_file, delimiter=args.delimiter)
    line = 0
    # rest of file contain new records
    for token in tokens:
       line += 1
       item = {}
       for i,val in enumerate(token):
         if val:
             print (val)
             object = s3.Object(bucket, '%s.txt' % line)
             object.put(Body=val)
