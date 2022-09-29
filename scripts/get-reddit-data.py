#!/usr/bin/env python

import sys
sys.path.append(os.path.join("..", "modules"))
import pushift_wrap as rapi

import os
import requests
import time
import random
import json
from json import JSONDecodeError
from datetime import datetime

# Pushift endpoints
sub_end = "https://api.pushshift.io/reddit/search/submission/"
subcomment_end = "https://api.pushshift.io/reddit/submission/comment_ids/"
comment_end = "https://api.pushshift.io/reddit/search/comment/"

# File out
name_out = "testdenmark.json" # filename for submissions (.json)
out_dir = os.path.join("..", "data")

if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

out_p = os.path.join(out_dir, name_out)

# Submissions search parameters
subreddits = ["denmark"] # input subreddits as list of strings without r/
start_time_epoch = int(datetime(2022,9,27,0,0).timestamp()) # input start of search time as epoch timestamp
end_time_epoch = int(datetime(2022,9,28,0,0).timestamp()) # input end of search time as epoch timestamp


# Get submissions
submissions = []
for subreddit in subreddits:
    new_submissions = rapi.get_submissions(subreddit = subreddit, before = end_time_epoch, after = start_time_epoch)
    submissions = submissions + new_submissions

    
# Get comments
for submission in submissions:
    
    subid = submission.get('id')
    
    request_url = f"{subcomment_end}{subid}"
    
    r = requests.get(request_url)

    while r.status_code != 200:
        
        counter = 0
        
        time.sleep(random.uniform(0.03, 0.10))

        r = requests.get(request_url)
        
        counter = counter + 1
        
        if counter > 10:
            break
    
    if r.status_code == 200:
        try:
            commentids = r.json().get('data')
            comments = rapi.get_comments(commentids)
        except JSONDecodeError:
            comments = []
            
    else:
        comments = []
    
    submission['comments'] = comments
            

# Save submissions
with open(out_p, 'w', encoding = 'utf-8') as f:
    json.dump(submissions, f)