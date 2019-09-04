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
# import jso
import hashlib
import instagram
import httplib2
import simplejson
import six
from instagram.client import InstagramAPI
import bottle
import beaker.middleware
from bottle import route, redirect, post, run, request, hook
from instagram import client, subscriptions

# client_id = "0b93b35efe26460ba4dab88096faa05f".strip()
# client_secret = "9fe62f1140464dd28653c4dc8a1c99c5".strip()
# redirect_url = "instagram.com/daniel.yoo"
# scope = 'basic'
# IG_api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_url)

# # user_id ='daniel.yoo'
# # redirect_uri = api.get_authorize_login_url(scope='public_content')
# # dir(client.InstagramAPI)

# # make sure you set the redirect uri to http://local
# accessUrl ="https://www.instagram.com/oauth/authorize/?client_id="+client_id+"&redirect_uri=http://"+"localhost"+"&response_type=code"
# accessUrl
# # retrieval_code  ="8dca7a1a70ab4464933cb12b1f9f4cc6"
# # retrieval_code="d811dc5be86846c3a32295c2f35bc24e"
# import urllib
# urllib.request.urlopen(accessUrl).read()
# dir(simplejson)
# import io
# import requests
# import html5lib 
# accessCode =requests.get(accessUrl)

# rawData = pd.read_csv(io.StringIO(accessCode.content.decode('utf-8')))
# pd.read_html(accessCode.content)
# accessCode.content
# # https://api.instagram.com/oauth/authorize/?client_id=CLIENT-ID&redirect_uri=REDIRECT-URI&response_type=token

# IG_api.exchange_code_for_access_token(retrieval_code)
# # curl https://www.instagram.com/explore/locations/212988663/?__a=1

urlTest="https://www.instagram.com/kyliejenner/?__a=1"


kylieId = '12281817'

tagging = "tagged"
user = 'kyliejenner'
urlTestTag="https://www.instagram.com/"+user+ "/"+tagging+"/?__a=1"
urlTestTag

# urlTest = "https://api.instagram.com/v1/users/"+kylieId+"/media/recent/?client_id="+client_id
from pandas.io.json import json_normalize

fetchedContent = requests.get(urlTest).content

# fetchedContent['graphql']['user']['biography']
# userColumns = [item for item in fetchedContent['graphql']['user']]
# flatContent = flatten_json(fetchedContent)
# pd.read_json(fetchedContent['graphql']['user'])

# pd.DataFrame.from_dict(fetchedContent['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]).transpose()
# DF_init = map( pd.DataFrame.from_dict, fetchedContent['graphql']['user']['edge_owner_to_timeline_media']['edges'])

timelineEdge = fetchedContent['graphql']['user']['edge_owner_to_timeline_media']['edges']
finalDF = pd.concat([pd.DataFrame.from_dict(row).transpose() for row in timelineEdge])

finalDF.thumbnail_src.values[1]

requests.get("https://www.instagram.com/kyliejenner/tagged/").content



def getEdge(url_in):
    fetched_content = requests.get(url_in).content
    fetched_content = simplejson.loads(fetched_content)
    edgeData = fetched_content['graphql']['user']['edge_owner_to_timeline_media']['edges']
    edgeDF = pd.concat([pd.DataFrame.from_dict(row).transpose() for row in edgeData])

    return edgeDF


tFetched_content = requests.get(urlTestTag).content
tFetched_content = simplejson.loads(tFetched_content)
tFetched_content['graphql']['shortcode_media']

fetchedContent['graphql']['shortcode_media']
taggedDF = getEdge("https://www.instagram.com/kyliejenner/tagged/"+"?__a=1")
taggedDF.thumbnail_src.values[1]

# [col for col in fetchedContent['graphql']['user'] if re.search('media',col)]

hashtagURL = "https://www.instagram.com/explore/tags/kyliejenner/?__a=1"

hashtagContent = simplejson.loads(requests.get(hashtagURL).content)
[col for col in hashtagContent['graphql']['hashtag']]

hashtagEdge = hashtagContent['graphql']['hashtag']['edge_hashtag_to_media']

def getHashtagEdge(hashtag):
    hashtagURL = "https://www.instagram.com/explore/tags/"+hashtag+"/?__a=1"
    fetched_content = requests.get(url_in).content
    fetched_content = simplejson.loads(fetched_content)
    edgeData = fetched_content['graphql']['hashtag']['edge_hashtag_to_media']['edges']
    edgeDF = pd.concat([pd.DataFrame.from_dict(row).transpose() for row in edgeData])

    return edgeDF


# hashtagDF = pd.concat([pd.DataFrame.from_dict(x).transpose() for x in hashtagEdge['edges']])
hashtagDF  = getHashtagEdge(hashtagURL)


def getUserInfo(inputuser):

    user_url = "https://i.instagram.com/api/v1/users/"+inputuser+"/info/"        
    user_content = requests.get(user_url).content
    user_content= simplejson.loads(user_content)
    if user_content['status'] =='ok':
        user_id=user_content['user']['username']
    else:
        time.sleep(90)
        user_content= simplejson.loads(user_content)
        user_id=user_content['user']['username']
    # userDF = pd.DataFrame.from_dict(user_content)
    
    try:
        user_profile_url = "https://www.instagram.com/"+user_id
        user_profile_content  = requests.get(user_profile_url).content
        user_profile_content = simplejson.loads(user_profile_content)
        followers = user_profile_content['graphql']['user']['edge_followed_by']
        following = user_profile_content['graphql']['user']['edge_follow']

    except:
        followers = np.nan
        following = np.nan

    outDF = pd.DataFrame(user_id, inputuser,followers, following )
    
    time.sleep(90)
    return outDF

# take owner id and pipe into this url https://i.instagram.com/api/v1/users/7795660123/info/

hashtagDF['ownervalue'] = hashtagDF.owner.apply(pd.Series)
hashtagDF['ownervalue'].values
hashtagDF['ownervalue'].apply( getUserInfo)
map(getUserInfo, hashtagDF['ownervalue'])

simplejson.loads(requests.get("https://i.instagram.com/api/v1/users/7795660123/info/").content)

# another link to check out
# https://www.instagram.com/web/search/topsearch/?context=blended&query=kyliejenner