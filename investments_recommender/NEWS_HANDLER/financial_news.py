from pprint import pprint
from finnews.client import News

# Create a new instance of the News Client.
news_client = News()

# Grab the CNBC News Client.
cnbc_news_client = news_client.cnbc

def get_news():
    # Grab the top news.
    news_data = cnbc_news_client.news_feed(topic='finance')
    return news_data    