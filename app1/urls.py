from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from app1 import views



urlpatterns = [
  path('', views.home, name='home'),
  path('DASHBOARD/', views.DASHBOARD, name='dashboard'),
  path('stocks/', views.stocks, name='stocks'),
  path('account/', views.account, name='account'),
  path('register/', views.register, name='register'),
  path('search/', views.search, name='search'),
]