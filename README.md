# aws-comprehend-demo
A set of short and simple demos for Amazon Comprehend

## detect.py
Detects sentiment for files stored in a S3 bucket and outputs results into [output_folder] as CSV file.
```
detect.py bucket [output_folder] [delimiter] [region]
```

## rss.py
Analyze a RSS feed and detects sentiment and key phrases for each item.
```
rss.py feed_url
```

## twitter.py
Analyze a twitter feed based on defined tag and detects sentiment for each item.
```
twitter.py tag [items_count=10] [region=us-east-1]
```
To run this demo create a ```secrets.py``` file with your twitter API credentials in the next format (**Make sure you don't share this files or commit it to public repos**):
```
api_key = '< API key >'
api_secret = '< API secret key >'
access_token = '< Access token >'
access_secret = '< Access secret token >'
```
