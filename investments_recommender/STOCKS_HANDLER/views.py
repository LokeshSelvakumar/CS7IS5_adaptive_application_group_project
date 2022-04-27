from django.shortcuts import render
import yfinance as yf
from yahoo_fin import stock_info as si
from django.http import JsonResponse
import pandas as pd
from firebase_admin import db
import json
import pandas as pd
# Create your views here.

tickers = si.tickers_sp500()
stocks_data = pd.read_csv('STOCKS_HANDLER/Stocks_data.csv')

def display_stocks(request):
    #This list has to be generated dynamically based on user preference.
    company_tickers_list = ["MSFT","AAPl","TSLA"]
    tickers_list = (" ").join(company_tickers_list)
    stock_price_data = yf.Tickers(tickers_list)
    result = {}
    for key,tickers in stock_price_data.tickers.items():
        result[key] = tickers.info
    return JsonResponse({"status":200,"data":result})

#Time consuming task - add it to a scheduler
def gather_stocks_data(request):
    stock_price_data = yf.Tickers(tickers)
    result = {}
    for key,tickers in stock_price_data.tickers.items():
        result[key] = tickers.info
    stocks_data = pd.DataFrame.from_dict(result)
    stocks_data = stocks_data.T
    target_columns = ['sector', 'longBusinessSummary', 'website', 'industry', 'profitMargins', 'grossMargins', 'operatingCashflow', 'revenueGrowth',  'recommendationKey', 'freeCashflow', 'currentPrice',  'debtToEquity', 'returnOnEquity','recommendationMean', 'symbol','beta','threeYearAverageReturn']
    stocks_data = stocks_data[target_columns]
    stocks_data.to_csv("Stocks_data.csv")
    return JsonResponse({"status":200})


#Sample User Data:
# user_data = {
#     'user_id' : 111,
#     'sector_preference' : [
#         'Technology'
#     ],
#     'available_captial': 2000,
#     'age' : 20,
#     'risk_preference': 'low_risk'
# }
def recommend_stocks(request):
    user_data = json.loads(request.body)
    user_id = str(user_data['user_id'])
    user_data = db.reference("/Users").get(user_id)[0][user_id]
    print(user_id)
    #Get the sector preference of the user
    intrested_sectors = user_data['sector_preference'][:3]
    data = []
    for sector in intrested_sectors:
        print(f"[INFO] RECOMMENDING STOCKS IN {sector}")
        stocks = stocks_data[
            (stocks_data['sector'] == sector) & 
            (stocks_data['Risk_Factor'] == user_data['risk_preference']) & 
            (stocks_data['currentPrice'] <= user_data['available_capital'])
        ]
        recommended_stocks = stocks.sort_values(by=['profitMargins'],ascending=False)
        target_columns = ['symbol','sector','Risk_Factor','currentPrice','profitMargins']
        recommended_stocks = recommended_stocks[target_columns]
        recommended_stocks = recommended_stocks.head(3)
        data.append(recommended_stocks)
    recommendations = pd.concat(data)
    recommendations_json = recommendations.to_json(orient='split')
    #Todo:Return a subset of recommendations.
    return JsonResponse({"status":True,"recommendations":json.loads(recommendations_json)},safe=False)


def suggest_day_gainers():
    data = si.get_day_gainers()
    #Add filtering here
    return data.head()

def get_user_stocks(request):
    user_data = json.loads(request.body)
    user_id = str(user_data['user_id'])
    user_data = db.reference("/Users").get(user_id)[0][user_id]
    
    #Process the user stocklist
    stocklist = {}
    for item in user_data['stockslist']:
        values = item.split(" ")
        stocklist[values[0].upper()] = float(values[1])
    stocks = stocks_data[stocks_data['symbol'].isin(stocklist.keys())]
    user_stocks = []
    for _,row in stocks.iterrows():
        name = row['symbol']
        currentPrice = row['currentPrice']
        currentValue = stocklist[name] * currentPrice
        currentValue = round(currentValue, 2)
        user_stocks.append({
            'Stock':name,
            'Current Price':currentPrice,
            'Current Value':currentValue,
        })

    #Process the user watchlist
    user_watchlist = []
    watchlist = user_data['watchlist']
    for i in range(len(watchlist)):
        watchlist[i] = watchlist[i].upper()
    stocks = stocks_data[stocks_data['symbol'].isin(watchlist)]
    for _,row in stocks.iterrows():
        name = row['symbol']
        currentPrice = row['currentPrice']
        user_watchlist.append({
            'Stock':name,
            'Current Price':currentPrice,
        })
    
    return JsonResponse({"status":True,"user_stocks":user_stocks,"user_watchlist":user_watchlist},safe=False)