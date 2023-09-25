from django.contrib import admin
from django.urls import path
from . import views
# app_name = 'NFTapp'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('home2/', views.home2, name='home2'),
    path('home5/', views.home5, name='home5'),
]
