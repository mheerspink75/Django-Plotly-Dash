from django.shortcuts import render
from app1.dashapps import crypto_charts
from app1.dashapps import stock_charts
from app1.dashapps import crypto_quotes


def home(request):
    return render(request, 'app1/pages/home.html')

def crypto(request):
    return render(request, 'app1/pages/crypto.html')

def stocks(request):
    return render(request, 'app1/pages/stocks.html')

def about(request):
    return render(request, 'app1/pages/about.html')