# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 13:46:17 2019

@author: Alex Richardson
"""

from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import random

api = PushshiftAPI()

#Picking Times
start_epoch=int(dt.datetime(2016, 1, 1).timestamp())
end_epoch=int(dt.datetime(2016, 12, 31).timestamp())

#Reading in Propaganda Usernames
usernames = pd.read_csv('table-of-usernames.csv')

#Looping through usernames to pull threads in the right epoch
threadlist = []
for n in usernames['Username']:
  templist = list(api.search_submissions(after = start_epoch,
                                         before = end_epoch,
                                         author=n
                                         ))
  threadlist.append(templist)

# Looping through those to clean the (wierdly) quick way
cleanest_threadlist = pd.DataFrame()
author = []
date = []
subreddit = []
title = []
url = []
post_id = []
num_comments = []
tholder = []
aholder = []
dholder = []
uholder = []
sholder = []
iholder = []
cholder = []
for n in threadlist:
    for o in n:
        author = o.author
        date = o.created
        title = o.title
        num_comments = o.num_comments
        try: 
            subreddit = o.subreddit
        except:
            subreddit = ""
        url = o.url
        try: 
            post_id = o.id
        except:
            post_id = ""
        tholder.append(title)
        aholder.append(author)
        dholder.append(date)
        uholder.append(url)
        sholder.append(subreddit)
        iholder.append(post_id)
        cholder.append(num_comments)

tholder = pd.DataFrame(tholder)
aholder = pd.DataFrame(aholder)
dholder = pd.DataFrame(dholder)
uholder = pd.DataFrame(uholder)
sholder = pd.DataFrame(sholder)
iholder = pd.DataFrame(iholder)
cholder = pd.DataFrame(cholder)

propthreads = pd.concat([tholder, aholder, dholder, uholder, sholder, iholder, cholder], axis=1)

#propthreads.to_csv("propthreads.csv")

# Pulling in gens for the users who responded to those
x=0
comment_author_list = []
for n in iholder[0]:
  print(n)
  temp2list = api.search_comments(
                            id=n,
                            filter=['author','id','subreddit','title']
                            )
  print(x)
  x += 1
  comment_author_list.append(temp2list)

# Reading those gens
caches_list = []
max_response_cache = 1000
cache = []
for c in comment_author_list:
    for d in c:
      cache.append(d)
      if len(cache) >= max_response_cache:
        break
    caches_list.append(cache)
    
caches_list.to_csv("authorset.csv")

# Run QuickClean.R here!

# Manually removed a few other automated accounts here after some trial and error (i.e. MTGCardFetcher)

py_comm_auth_list = pd.read_csv('Comment-Author-List-Clean-2.csv') 

# Obtaining gens for exposed authors' comment histories
x = 0
comment_history_gen = []
for n in py_comm_auth_list['Author']:
  temp3list = api.search_comments(after=start_epoch,
                            before=end_epoch,
                            author=n
                            )
  print(x)
  x += 1
  comment_history_gen.append(temp3list)
  
  
# Reading those gens
hist_caches_list = []
for c in comment_history_gen:
    hist_cache = []
    for d in c:
        hist_cache.append(d)
        print(d)
    hist_caches_list.append(hist_cache)
    
# Looping through these to clean the elegant, but kind of slow way
dataset = pd.DataFrame()
x = 0
for n in hist_caches_list:
    for o in n:
        dataset = dataset.append(pd.DataFrame(o.d_, index=[x]))
        print(x)
        x+=1
        
dataset.to_csv('dataset.csv')

##################### Random Control Set ###########################

def randate(start, end):
    return start + dt.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
    
start_date = dt.datetime(2016, 1, 1)
end_date = dt.datetime(2016, 12, 31)

random_subreddits = pd.read_csv('randomSubreddits.csv')

#Looping through random subreddits starting from a random date in the epoch to pull random threads matching exposed user patterns
rand_threadlist = []
x=0
for n in random_subreddits['randomSubreddits']:
  templist = list(api.search_submissions(after = int(randate(start_date, end_date).timestamp()),
                                         before = end_epoch,
                                         subreddit = n,
                                         limit=1
                                         ))
  print(x)
  x+=1
  rand_threadlist.append(templist)
  
# Looping through those to clean the quick way - random
rand_clean_threadlist = pd.DataFrame()
author = []
date = []
subreddit = []
title = []
url = []
post_id = []
num_comments = []
tholder = []
aholder = []
dholder = []
uholder = []
sholder = []
iholder = []
cholder = []
for n in rand_threadlist:
    for o in n:
        author = o.author
        date = o.created
        title = o.title
        num_comments = o.num_comments
        try: 
            subreddit = o.subreddit
        except:
            subreddit = ""
        url = o.url
        try: 
            post_id = o.id
        except:
            post_id = ""
        tholder.append(title)
        aholder.append(author)
        dholder.append(date)
        uholder.append(url)
        sholder.append(subreddit)
        iholder.append(post_id)
        cholder.append(num_comments)

tholder = pd.DataFrame(tholder)
aholder = pd.DataFrame(aholder)
dholder = pd.DataFrame(dholder)
uholder = pd.DataFrame(uholder)
sholder = pd.DataFrame(sholder)
iholder = pd.DataFrame(iholder)
cholder = pd.DataFrame(cholder)

randthreads = pd.concat([tholder, aholder, dholder, uholder, sholder, iholder, cholder], axis=1)


# Pulling in gens for the users who responded to those - random
x=0
comment_random_list = []
for n in iholder[0]:
  print(n)
  temp2list = api.search_comments(
                            id=n,
                            filter=['author','id','subreddit','title']
                            )
  print(x)
  x += 1
  comment_random_list.append(temp2list)

# Reading those gens
rand_caches_list = []
max_response_cache = 1000
cache = []
for c in comment_author_list:
    for d in c:
      cache.append(d)
      if len(cache) >= max_response_cache:
        break
    caches_list.append(cache)
    
rand_caches_list.to_csv("rand_authorset.csv")

# Run QuickClean.R here!

rand_comm_auth_list = pd.read_csv('Comment-Author-List-Clean-rand.csv') 

# Obtaining gens for random authors' comment histories
x = 0
rand_comment_history_gen = []
for n in rand_comm_auth_list['Author']:
  temp3list = api.search_comments(after=start_epoch,
                            before=end_epoch,
                            author=n
                            )
  print(x)
  x += 1
  rand_comment_history_gen.append(temp3list)
  
  
# Reading those gens
rand_hist_caches_list = []
for c in comment_history_gen:
    hist_cache = []
    for d in c:
        hist_cache.append(d)
        print(d)
    rand_hist_caches_list.append(hist_cache)
    
# Looping through these to clean 
randset = pd.DataFrame()
x = 0
for n in rand_hist_caches_list:
    for o in n:
        randset = randset.append(pd.DataFrame(o.d_, index=[x]))
        print(x)
        x+=1
        
randset.to_csv('control_dataset.csv')