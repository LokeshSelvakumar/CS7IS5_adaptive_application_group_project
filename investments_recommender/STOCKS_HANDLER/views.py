from django.shortcuts import render
import yfinance as yf
from yahoo_fin import stock_info as si
from django.http import JsonResponse
import pandas as pd
# Create your views here.

tickers = si.tickers_sp500()

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
def recommend_stocks(stocks_data,user_data):
    #Get the sector preference of the user
    intrested_sectors = user_data['sector_preference']
    data = []
    for sector in intrested_sectors:
        print(f"[INFO] RECOMMENDING STOCKS IN {sector}")
        stocks = stocks_data[
            (stocks_data['sector'] == sector) & 
            (stocks_data['Risk_Factor'] == user_data['risk_preference']) & 
            (stocks_data['currentPrice'] <= user_data['available_captial'])
        ]
        recommended_stocks = stocks.sort_values(by=['profitMargins'],ascending=False)
        target_columns = ['sector','Risk_Factor','currentPrice','profitMargins']
        recommended_stocks = recommended_stocks[target_columns]
        data.append(recommend_stocks)
    recommendations = pd.concat(data)
    #Todo:Return a subset of recommendations.
    return recommendations
