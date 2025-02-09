import praw
import json
import requests
from bs4 import BeautifulSoup
import re
import os
import validators
import concurrent.futures
import threading
import queue
import time

# Function to create a Reddit instance
def redditObjectCreator(jsonFile="reddit_config.json", json_key="reddit"):
    with open(jsonFile, 'r') as f:
        config = json.load(f)
    reddit_credentials = config[json_key]
    reddit = praw.Reddit(
        client_id=reddit_credentials['client_id'],
        client_secret=reddit_credentials['client_secret'],
        user_agent=reddit_credentials['user_agent'],
        username=reddit_credentials['username'],
        password=reddit_credentials['password'],
        # handling 429 errors
        ratelimit_seconds=60
    )
    return reddit

# Function to extract URLs from post body text
# can use this feature add an extra field showing urls in posts and comment sections
def extract_urls(text):
    pattern = re.compile(r'(https?://[^\s\)\]\}]+)')
    return [match for match in re.findall(pattern, text) if validators.url(match)]

def is_file_size_exceeded():
    return os.path.exists('mt_data.json') and os.path.getsize('mt_data.json') >= (50*1024*1024)

## data aggregator

thq = queue.Queue()
def agg(submission):
    com_rep = []
    urls = extract_urls(submission.selftext)
    if not submission.stickied:
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            com_rep.append(comment.body)

    data = { "id": str(submission.id),
            "title": str(submission.title),
            "author": str(submission.author),
            "body": submission.selftext,
            "comments": com_rep,
            "ups": str(submission.ups),
            "downs": str(submission.downs)
            }
    thq.put(data)
    # this method was overwriting on the same file. -> collosal time waste
    # with results_lock:
    #     with open("mt_data.json", "w", encoding="utf-8") as file:
    #         json.dump(data, file, indent=4)

def multi_crawl(sub):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        # using 'top' and 'hot' takes time -> should be done for more data
        for sort_type in ['new']:
            for submission in sub.__getattribute__(sort_type)(limit=200):
                futures.append(executor.submit(agg, submission))

        # Wait for all threads to complete
        for future in futures:
            future.result()

        # writing to json file after all threads are done
        file_writer()

def file_writer():
    if thq.empty():
        return

    data = []
    while not thq.empty():
        data.append(thq.get())

    # Thread-safe writing: Append new data properly formatted in JSON
     # Ensures only one thread writes
    with threading.Lock():
        if os.path.exists("mt_data_v2.json") and os.path.getsize("mt_data_v2.json") > 0:
            with open("mt_data_v2.json", "r+", encoding="utf-8") as file:
                try:
                    current = json.load(file)
                    if not isinstance(current, list):
                        current = []
                except json.JSONDecodeError:
                    current = []
                # all of data so far
                current.extend(data)

                # updating old data to current data by appending newly acquired data
                # Move cursor to beginning of file
                # we are doing this because 'a' option is unavailable , JSON doesnt support appending operation like we want
                file.seek(0)
                json.dump(current, file, indent=4)
        else:
            with open("mt_data_v2.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

reddit = redditObjectCreator()
sub = reddit.subreddit("cscareerquestions")
multi_crawl(sub)
# crawl(sub)
