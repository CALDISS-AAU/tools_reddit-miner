#!/usr/bin/env python

import requests
import time
import random
import os 
import json
from json import JSONDecodeError
import math

sub_end = "https://api.pushshift.io/reddit/search/submission/"
subcomment_end = "https://api.pushshift.io/reddit/submission/comment_ids/"
comment_end = "https://api.pushshift.io/reddit/search/comment/"

def get_submissions(subreddit, before, after, q = "", size = 499, fields = ['author', 'created_utc', 'domain', 'full_link', 'gildings', 'id', 'is_original_content', 'is_reddit_media_domain', 
                                                                           'locked', 'media_only', 'num_comments', 'num_crossposts', 'over_18', 'permalink', 'pinned', 'post_hint', 'preview', 
                                                                           'retrieved_on', 'score', 'selftext', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_subscribers',
                                                                           'subreddit_type', 'thumbnail', 'title', 'total_awards_received', 'upvote_ratio', 'url', 'url_overridden_by_dest',
                                                                           'comments']):
    
    endpoint = "https://api.pushshift.io/reddit/search/submission/"
    fields_str = ','.join(fields)
    
    start_time = after
    end_time = before
    
    # Split time period into intervals
    interval = int(0.5 * 86400) # half a day
    
    from_time_epoch = start_time

    submissions = []
    while from_time_epoch <= end_time:

        to_time_epoch = from_time_epoch + interval 
        
        request_url = f"{endpoint}?subreddit={subreddit}&before={to_time_epoch}&after={from_time_epoch}&size={size}&q={q}&fields={fields_str}"
        
        r = requests.get(request_url)
        
        while r.status_code != 200:
            
            time.sleep(random.uniform(0.03, 0.10))
            
            r = requests.get(request_url)
        
        new_submissions = r.json().get('data')
        submissions = submissions + new_submissions
        
        from_time_epoch = to_time_epoch

        time.sleep(random.uniform(0.03, 0.10))
        
    return(submissions)
    
def get_comments(commentids, fields = ['author', 'banned_at_utc', 'body', 'collapsed', 'collapsed_reason', 'comment_type', 'created_utc', 'edited', 'id', 'is_submitter',
                 'link_id', 'parent_id', 'permalink', 'retrieved_on', 'score', 'stickied', 'subreddit', 'subreddit_id', 'total_awards_received']):
    
    endpoint = 'https://api.pushshift.io/reddit/search/comment/'
    
    max_ids = 500
    split = math.ceil(len(commentids)/max_ids)

    comment_fields_str = ','.join(fields)

    comments = []
    for i in range(split):
        ids_chunk = commentids[i*max_ids:(i+1)*max_ids]
        commentids_str = ','.join(ids_chunk)

        request_url = f"{endpoint}?ids={commentids_str}&fields={comment_fields_str}"
        
        r = requests.get(request_url)
        
        while r.status_code != 200:
            
            time.sleep(random.uniform(0.03, 0.10))
            
            r = requests.get(request_url)
            
        comments_chunk = r.json().get('data')
        comments = comments + comments_chunk
        
        time.sleep(random.uniform(0.03, 0.10))
        
    return(comments)