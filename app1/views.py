from django.shortcuts import render, redirect
from .forms.forms import RegisterForm
from app1.dashapps import stock_charts2
from app1.dashapps import crypto_quotes


def home(request):
    return render(request, 'app1/pages/index.html')

def DASHBOARD(request):
    return render(request, 'app1/pages/DASHBOARD.html')


def crypto(request):
    return render(request, 'app1/pages/crypto.html')


def stocks(request):
    return render(request, 'app1/pages/stocks.html')


def about(request):
    return render(request, 'app1/pages/about.html')

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = RegisterForm()

    return render(response, 'registration/register.html', {"form":form})
