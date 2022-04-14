from django.shortcuts import render
from django.http import JsonResponse
from .financial_news import *

# Create your views here.
def display_news(request):
    news_data = get_news()
    return JsonResponse({"status":200,"news":news_data})