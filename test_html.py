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
from bs4 import BeautifulSoup
urlKylie = "https://www.instagram.com/kyliejenner/"

JsonOut = requests.get(urlKylie).content
soup = BeautifulSoup(JsonOut)
soup
# [soup.findAll('a',attrs = {'href':re.compile("^http://")},link) for link in soup]
soup.findAll('a',attrs = {'href':re.compile("config")})
help(soup.findall)
# for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):


