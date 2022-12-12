import requests
from bs4 import BeautifulSoup
import re

client_id = "nBNUFySa1GTQOQBaITmgUA"
secret = "YXnEdLh4APgv93l8TteMXF8Ny_X76Q"
user_agent="WPScraper"
url = "https://www.reddit.com/r/WritingPrompts/comments/zhurxo/wp_as_a_villain_henchman_the_number_1_rule_youre/"

import praw
import pandas as pd


def grab_top_posts(subreddit, top_num):
    reddit_read_only = praw.Reddit(client_id=client_id,		 # your client id
							client_secret=secret,	 # your client secret
							user_agent=user_agent)	 # your user agent

    subreddit = reddit_read_only.subreddit("WritingPrompts")
    num_posts =0
    for post in subreddit.hot(limit=top_num):
        
        if "[WP]" not in post.title:
            continue
        num_posts += 1
        print(post.title)
        i=0
        for comment in post.comments[1:]:
            if comment.author is None:
                continue
            i+=1
            if i > 1 :
                continue
            print(f"Story {i} written by {comment.author}")
            story = _censor(comment.body)
            print(story)
        print(num_posts)

def count_sentences(string):
  sentences = re.split(r"\.+", string)
  num_sentences = len(sentences)
  return num_sentences

def _censor(text):
  # Define a dictionary that maps expletives to safe alternatives
  replacements = {
    "damn": "dang",
    "hell": "heck",
    "crap": "junk",
    "fuck": "fudge",
    "shit": "crap",
    "cunt": "jerk",
    "cum": "semen",
    "ass": "rear end"
  }
  
  # Use a regular expression to find and replace expletives with their safe alternatives
  censored_text = re.sub(r"\b(" + "|".join(replacements.keys()) + r")\b", lambda m: replacements[m.group(0)], text)
  
  return censored_text

grab_top_posts("WritingPrompts", 3)