from django.contrib import admin
from django.urls import path
from . import views
from . import function
# app_name = 'NFTapp'
urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_page, name="register"),
    path('edit-profile/', views.edit_profile, name="edit_profile"),
    path('search-result/', views.search_result, name="search_result"),
    path('trade-history/', views.trade_history, name="trade_history"),
    
    path('home1/', views.home1, name='home1'),
    path('home2/', views.home2, name='home2'),
    path('home3/', views.home3, name='home3'),
    path('home4/', views.home4, name='home4'),
    path('home5/', views.home5, name='home5'),
    
    path('collection1/', views.collection1, name='collection1'),
    path('collection2/', views.collection2, name='collection2'),
    path('collection3/', views.collection3, name='collection3'),
    path('collection4/', views.collection4, name='collection4'),
    path('collection5/', views.collection5, name='collection5'),
    
    path('collection1/<uuid:pk>/', views.collection_detail_1, name='collection1'),

    path('artworks1/', views.artworks1, name='artworks1'),
    path('artworks2/', views.artworks2, name='artworks2'),
    path('artworks3/', views.artworks3, name='artworks3'),
    path('artworks4/', views.artworks4, name='artworks4'),
    path('artworks5/', views.artworks5, name='artworks5'),

    path('about_us1/', views.about_us1, name='about_us1'),
    path('about_us2/', views.about_us2, name='about_us2'),
    path('about_us3/', views.about_us3, name='about_us3'),
    path('about_us4/', views.about_us4, name='about_us4'),
    path('about_us5/', views.about_us5, name='about_us5'),

    path('artists/', views.artists, name='artists'),
    path('editorial/', views.editorial, name='editorial'),

    path('FAQs1/', views.FAQs1, name='FAQs1'),
    path('FAQs2/', views.FAQs2, name='FAQs2'),
    path('FAQs3/', views.FAQs3, name='FAQs3'),
    path('FAQs4/', views.FAQs4, name='FAQs4'),
    path('FAQs5/', views.FAQs5, name='FAQs5'),
    
    path('blog/', views.blog, name='blog'),
    path('blog/<uuid:pk>/', views.blog_detail, name='blog'),

    path('profile/<uuid:pk>/', views.profile, name='profile'),
]
