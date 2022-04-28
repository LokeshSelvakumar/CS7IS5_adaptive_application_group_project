# -*- coding = utf-8 -*-
# @Time : 27/04/2022 15:16
# @Author : Yan Zhu
# @File : tg_sendnews.py
# @Software : PyCharm
import time

import telebot
import yfinance as yf
from yahoo_fin import stock_info as si
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types
import requests
import json
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import os

privatekeypath = os.path.dirname(os.getcwd())
privatekeypath = os.path.join(privatekeypath,'investments_recommender/investments_recommender/static/privateKey.json')
cred_obj = credentials.Certificate(privatekeypath)

default_app = firebase_admin.initialize_app(cred_obj, {
'databaseURL': 'https://adaptive-application-default-rtdb.firebaseio.com/'
})

bot = telebot.TeleBot("5356735903:AAGIUWFapkm7AcpAhyV44n-yojw1Sa3CNl0")
ref = db.reference("/Users")
users = ref.get()

# @bot.message_handler(commands=['start', 'help'])
def send_news():
    user_id = '1950809226'
    ref = db.reference("/Users")
    users = ref.get()
    ref = users[user_id]['sector_preference']
    print(ref)
    API_KEY = 'fb3a5891a786455bb898f36e92b09f24'

    bot.send_message(user_id, "Good Evening! Here are the news articles you may be interested in.")
    time.sleep(1)
    # for item in ref:
    params = {
        # 'q': 'war',
        'source': 'bbc-news',
        'sortBy': 'top',
        'language': 'en',
        'category': 'health',
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
    results = [arr["title"] for arr in articles]
    links = [arr["url"] for arr in articles]
    results = results[:5]
    links = links[:5]
    for i in range(len(results)):
        bot.send_message(user_id, str(i + 1) + ". " + str(results[i]) + "\n" + str(links[i]), parse_mode='HTML')
        time.sleep(2)

def send_stock():
    user_id = '1950809226'
    API_KEY = 'fb3a5891a786455bb898f36e92b09f24'

    bot.send_message(user_id, "Good evening! This is today's gainers!")
    data = si.get_day_gainers()
    data = data.head()
    result = ""
    for index, row in data.iterrows():
        result += row['Symbol'] + ":" + str(round(float(row["Price (Intraday)"]),2))+"\n"
    bot.send_message(user_id, result)

send_news()
send_stock()