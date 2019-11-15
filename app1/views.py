from django.shortcuts import render
from app1.dashapps import dashtable

# Create your views here.

def home(request):
    return render(request, 'app1/pages/home.html')

def about(request):
    return render(request, 'app1/pages/about.html')