# aws-comprehend-demo

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
