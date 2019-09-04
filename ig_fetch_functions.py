import pandas as pd
import numpy as np
import os
# import sklearn
import re
import zipfile
import sys
# import urllib2
import requests
import random
import time
import hashlib
import instagram
import httplib2
import simplejson
from pandas.io.json import json_normalize
import datetime
# import six
# from instagram.client import InstagramAPI
# import bottle
# import beaker.middleware
# from bottle import route, redirect, post, run, request, hook
# from instagram import client, subscriptions


# grabs the most recent posts with a given hashtag
def getHashtagEdge(hashtag):
    
    hashtagURL = "https://www.instagram.com/explore/tags/"+hashtag+"/?__a=1"
    fetched_content = requests.get(hashtagURL).content
    fetched_content = simplejson.loads(fetched_content)
    edgeData = fetched_content['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    edgeDF = pd.concat([pd.DataFrame.from_dict(row).transpose() for row in edgeData])
    
    edgeDF['edge_liked_by'] = edgeDF['edge_liked_by'].apply(pd.Series)
    edgeDF['edge_media_preview_like'] = edgeDF['edge_media_preview_like'].apply(pd.Series)
    edgeDF['video_view_count'] = edgeDF['video_view_count'].apply(pd.Series)
    edgeDF['owner'] = edgeDF['owner'].apply(pd.Series)
    edgeDF['taken_at_timestamp']= pd.to_datetime(edgeDF['taken_at_timestamp'],unit = 's')    
    edgeDF['hashtag'] = hashtag
    return edgeDF



def getUserInfo(inputuser):

    user_url = "https://i.instagram.com/api/v1/users/"+inputuser+"/info/"        
    user_content = requests.get(user_url).content
    user_content= simplejson.loads(user_content)
    if user_content['status'] =='ok':
        user_id=user_content['user']['username']
    else:
        # pretty sure status will not return 'ok' if we continue to cycle through continuously. 
        # set conservative break of 90 seconds between each loop. validate this suspicion to be sure
        time.sleep(90)
        user_content= simplejson.loads(user_content)
        user_id=user_content['user']['username']
    
    try:
        dictOut = {'user_id':user_id, 'inputuser':inputuser}
        user_profile_url = "https://www.instagram.com/"+user_id+"/?__a=1"
        user_profile_content  = requests.get(user_profile_url).content
        user_profile_content = simplejson.loads(user_profile_content)
        dictOut['followers'] = str(user_profile_content['graphql']['user']['edge_followed_by']['count'])
        dictOut['following'] = str(user_profile_content['graphql']['user']['edge_follow']['count'])

    except:
        # pretty sure if nothing is returned, user is private. validate to be sure, using the usere_profile_content object
        followers = np.nan
        following = np.nan

    outDF = pd.DataFrame(dictOut, index = [0])
    
    time.sleep(10)
    return outDF




