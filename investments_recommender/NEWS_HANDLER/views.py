import requests
from django.shortcuts import render
from django.http import JsonResponse
# from .financial_news import *
import json
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import os

"""
privatekeypath = os.path.dirname(os.getcwd())
privatekeypath = os.path.join(privatekeypath,'investments_recommender/static/privateKey.json')
cred_obj = credentials.Certificate(privatekeypath)

default_app = firebase_admin.initialize_app(cred_obj, {
'databaseURL': 'https://adaptive-application-default-rtdb.firebaseio.com/'
})"""

# Create your views here.
# Topics that can be queried: 'business', 'technology', 'science', 'entertainment', 'health', 'sports'
def display_news(request):
    user_data = json.loads(request.body)
    user_id = str(user_data['user_id'])
    ref = db.reference("/Users")
    users = ref.get()
    ref = users[user_id]['sector_preference']

    # Get news of interest to users
    API_KEY = 'fb3a5891a786455bb898f36e92b09f24'

    # Get news according to users' different topics of interest, displaying news items(title) per topic
    params = {
        # 'q': '',
        'source': 'bbc-news',
        'sortBy': 'relevancy',
        'language': 'en',
        'category': ref[0],
        # 'country': 'us',
        # 'apiKey': API_KEY,
    }

    headers = {
        'X-Api-Key': API_KEY,  # KEY in header to hide it from url
    }

    url = 'https://newsapi.org/v2/top-headlines'

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    articles = data["articles"]
    news_data = json.dumps(articles, indent=4)
    return JsonResponse({"status":200,"news":news_data})