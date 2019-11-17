from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from app1 import views

urlpatterns = [
  path('', views.home, name='home'),
  path('crypto/', views.crypto, name='crypto'),
  path('stocks/', views.stocks, name='stocks'),
  path('about/', views.about, name='about'),
]