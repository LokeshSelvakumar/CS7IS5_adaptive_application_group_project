from django.shortcuts import render
import yfinance as yf
from django.http import JsonResponse
# Create your views here.



def display_stocks(request):
    #This list has to be generated dynamically based on user preference.
    company_tickers_list = ["MSFT","AAPl","TSLA"]
    tickers_list = (" ").join(company_tickers_list)
    stock_price_data = yf.Tickers(tickers_list)
    result = {}
    for key,tickers in stock_price_data.tickers.items():
        result[key] = tickers.info
    return JsonResponse({"status":200,"data":result})