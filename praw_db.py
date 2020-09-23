import os
from dotenv import load_dotenv
import sqlite3
import praw
import time
import numpy as np

# Create db schema
# Defining a function to refresh connection and cursor
def refresh_connection_and_cursor():
  try:
    c.close()
    conn.close()
  except: pass
  conn = sqlite3.connect('subreddit_db.sqlite3')
  c = conn.cursor()
  return conn, c

conn, c = refresh_connection_and_cursor()

c.execute('drop table if exists submission_table')
c.execute('''create table submission_table (
               subreddit_name text,
               subreddit_id text,
               title text,
               text text
             )
             ''')

# instantiate praw
load_dotenv()
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     user_agent='veggiecode')

sleep_min = 2
sleep_max = 5
start_time = time.time()

subreddit_count = 0

sub_list = ['announcements', 'funny', 'AskReddit', 'gaming', 'Music', 'science',
            'worldnews', 'movies', 'news', 'Showerthoughts',
            'food', 'books', 'LifeProTips', 'Art',
            'mildlyinteresting', 'DIY', 'sports', 'nottheonion', 'space', 'gadgets',
            'Documentaries', 'GetMotivated', 'television', 'history', 'personalfinance',
            'TwoXChromosomes', 'technology', 'AdviceAnimals', 'Fitness', 'politics',
            'WTF', 'travel', 'programming', 'PublicFreakout', 'Parenting', 'Coronavirus',
            'Cooking', 'cars', 'biology', 'scifi', 'socialskills', 'entertainment',
            'JusticeServed', 'Design', 'camping', 'literature', 'HomeImprovement',
            'conspiracy', 'math', 'MachineLearning', 'worldpolitics',
            'Health', 'investing']

reddit.subreddit("all").hot()

# for subreddit in reddit.subreddits.popular(limit=200):
for name in sub_list:
    subreddit = reddit.subreddit(name)
    records = []
    for submission in subreddit.top(limit=1000):
        records.append([subreddit.display_name, subreddit.id, submission.title, submission.selftext])
    print(records[0])
    c.executemany('''insert into submission_table
                  (subreddit_name, subreddit_id, title, text)
                  values (?, ?, ?, ?)
                  ''', records)
    conn.commit()
    subreddit_count += 1
    if subreddit_count % 5 == 0:
        time.sleep(np.random.uniform(sleep_min, sleep_max))
        print('Count: {} , Subreddit: {} added'.format(subreddit_count, subreddit))
        print('Elapsed Time: {} seconds'.format(time.time() - start_time))


c.close()
conn.close()