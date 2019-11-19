from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns =[
    path("register/", views.register, name="register")
]