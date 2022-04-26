from django.shortcuts import render
from django.http import JsonResponse
from .financial_news import *
from firebase_admin import db
import json

# Create your views here.
# Topics that can be queried: 'business', 'technology', 'science', 'entertainment', 'health', 'sports'
def display_news(request):
    user_data = json.loads(request.body)
    user_id = str(user_data['user_id'])
    ref = db.reference("/Users")
    users = ref.get()
    ref = users[user_id]['sector_reference']

    # Get news of interest to users
    API_KEY = 'fb3a5891a786455bb898f36e92b09f24'

    # Get news according to users' different topics of interest, displaying news items(title) per topic
    for item in ref:
        params = {
            # 'q': '',
            'source': 'bbc-news',
            'sortBy': 'relevancy',
            'language': 'en',
            'category': item,
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
        news_data = json.loads(articles)
    return JsonResponse({"status":200,"news":news_data})