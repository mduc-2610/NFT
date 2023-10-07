from django.contrib import admin
from django.urls import path
from . import views
# app_name = 'NFTapp'
urlpatterns = [
    path('home1/', views.home, name='home1'),
    path('home2/', views.home2, name='home2'),
    path('home5/', views.home5, name='home5'),
    path('collection1/', views.collection1, name='collection1'),
    path('collection2/', views.collection2, name='collection2'),
    path('collection3/', views.collection3, name='collection3'),
    path('collection4/', views.collection4, name='collection4'),
    path('collection5/', views.collection5, name='collection5'),
    path('blog/', views.blog, name='blog'),
    path('blog/<uuid:pk>', views.blog_detail, name='blog'),
]
