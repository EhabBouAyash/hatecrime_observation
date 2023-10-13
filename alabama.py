import pandas as pd
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime, timezone
import time
import matplotlib.pyplot as plt
import pytz
import praw

'''
i will conduct this study on massachusetts since its my home state and its one of the safest states in the US
I chose a safe state to demonstrate the increase in crime rate if there is a prominent amount 
of hate speech or hateful language present
'''
def change_time(x):
    dateobj = datetime.fromtimestamp(x,tz=timezone.utc)
    eastern_timezone = pytz.timezone('America/New_York')
    local_datetime = dateobj.astimezone(eastern_timezone)
    return local_datetime

user_agent = "Scraper 1.0 by /u/Ayhayb"
reddit = praw.Reddit(
    client_id='bopCDRmthtWgy6M6kaQYDA',
    client_secret='4rH7X3w-lpXFAI3FOAuDusjqmrNm7g',
    user_agent=user_agent
)

maxdate = datetime(2023,10,10)
def dump_into(alabama_set,maxdate):
    name = "alabama"
    subreddit = reddit.subreddit(name)
    minimum_date = datetime(2020,1,1)
    while True: 
        posts = reddit.subreddit('alabama').hot(limit=100, params={'after': minimum_date})
        for post in posts:
            if datetime.fromtimestamp(minimum_date)<=datetime.fromtimestamp(post.created_utc):
                submission = reddit.submission(id=post.id)
                try:
                    cmts = [(comment.body,comment.created_utc) for comment in submission.comments]
                except AttributeError:
                    continue
                try:
                    alabama_set.add((post.title,post.created_utc,post.upvote_ratio,post.selftext,post.score,tuple(cmts)))
                except TypeError:
                    continue
                maxdate=post.created_utc
            elif datetime.fromtimestamp(post.created_utc)<minimum_date:
                exit()
        time.sleep(4)

    
            



def make_dataframe(alabama_set):
    with open("alabama_info.pkl", 'rb') as f:
        alabama_set = pickle.load(f)
    df = pd.DataFrame(alabama_set)
    df.columns= ['title', 'date','upvote ratio', 'content','upvote score','comments']
    df['date'] = pd.to_datetime(df['date'], unit='s') 
    df_sorted = df.sort_values(by='date')
    return df_sorted

#we open the file to make the dataframe
#with open("alabama_info.pkl", 'rb') as f:
#    alabama_set = pickle.load(f)
#df = make_dataframe(alabama_set)
#df.sort_values(by='date')
#print(df['date'].iloc[-1])
#maxdate = min(df['date']) #record 0 is the oldest date so far. 
# we need to feed it to the dump_into function and make it less than the maxdate and greater than minimum 
#we extract the pickle file just so that we can sort it and get the greatest date and then perform the dumping again
#however we can just get the oldest date with min function
with open('alabama_info.pkl', 'rb') as f:
    alabama_set = pickle.load(f)
dump_into(alabama_set,maxdate)

