import json
from pprint import pprint
from finnews.client import News
from yahoo_fin.stock_info import *

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

file_name = ["CNBC", "NASDAQ", "MarketWatch", "SPGlobal", "SeekingAlpha", "CNNFinance", "YahooFinance"]
news_categorzation = ['finance', 'energy', 'media']
# Create a new instance of the News Client.
news_client = News()


def save_file(file_name, news_data):
    with open(file="../NEWS_HANDLER/news_data/"+file_name+".json", mode='w', encoding="utf-8") as f:
        json.dump(news_data, f, indent=4)


def cnbc(topic):
    # Grab the finance news.
    cnbc_news_client = news_client.cnbc
    news_data = cnbc_news_client.news_feed(topic=topic)
    return news_data


def nasdaq():
    nasdaq_client = news_client.nasdaq
    news_data = nasdaq_client.nasdaq_news_feed()
    return news_data


def market_watch():
    market_watch_client = news_client.market_watch
    news_data = market_watch_client.stocks_to_watch()
    return news_data


def sp_global():
    sp_global_client = news_client.sp_global
    news_data = sp_global_client.corporate_news()
    return news_data


def seeking_alpha():
    seeking_alpha_client = news_client.seeking_alpha
    news_data = seeking_alpha_client.latest_articles()
    return news_data


def cnn_finance():
    cnn_finance_client = news_client.cnn_finance
    news_data = cnn_finance_client.economy()
    return news_data


def yahoo_finance():
    yahoo_finance_client = news_client.yahoo_finance
    news_data = yahoo_finance_client.headlines("stocks")
    return news_data


def get_news():
    # save_file(file_name[0], cnbc())
    save_file(file_name[1], nasdaq())
    save_file(file_name[2], market_watch())
    save_file(file_name[3], sp_global())
    save_file(file_name[4], seeking_alpha())
    save_file(file_name[5], cnn_finance())
    save_file(file_name[6], yahoo_finance())


def categorization():
    for item in news_categorzation:
        with open(file="../NEWS_HANDLER/news_data/cnbc/" + item + ".json", mode='w', encoding="utf-8") as f:
            json.dump(cnbc(item), f, indent=4)

def get_trending_stock():
    trending_stock = dict()
    company = tickers_sp500(include_company_data = False)
    for i in range(len(company)):
        trending_stock[company[i]] = get_live_price(company[i])
    print(trending_stock)
    with open(file="../NEWS_HANDLER/stock_data/live_price_500.json", mode='w', encoding="utf-8") as f:
        json.dump(trending_stock, f, indent=4)

def abbreviation_to_full():
    abbreviation_to_full = dict()
    company_data = tickers_sp500(include_company_data=True)
    for indexs in company_data.index:
        abbreviation_to_full[company_data.loc[indexs].values[0]] = company_data.loc[indexs].values[1]
    with open(file="../NEWS_HANDLER/stock_data/abbreviation_to_full_500_companies.json", mode='w', encoding="utf-8") as f:
        json.dump(abbreviation_to_full, f, indent=4)




abbreviation_to_full()
