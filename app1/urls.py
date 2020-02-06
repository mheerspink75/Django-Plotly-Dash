from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from app1 import views



urlpatterns = [
  path('', views.home, name='home'),
  path('DASHBOARD/', views.DASHBOARD, name='dashboard'),
  path('markets/', views.markets, name='markets'),
  path('crypto_news/', views.crypto_news, name='crypto_news'),
  path('register/', views.register, name='register'),
  path('quotes/', views.quotes, name='quotes'),
  path('test_page/', views.test_page, name='test_page')
]