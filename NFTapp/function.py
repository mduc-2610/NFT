from collections import Counter
from math import ceil
import random
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Count
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite


def cal_times_to_read(blogs):
    average_wpm = 238
    blogs_context = {}
    for blog in blogs:
        words_of_blog = sum([len(str(section.content).split()) for section in blog.blog_section.all()])
        blogs_context[blog] = ceil(words_of_blog / average_wpm)
    return blogs_context

rarity = {}
def product_rarity():
    rarity = {}
    products = NFTProduct.objects.all().order_by('rarity')
    cnt = 1
    for product in products:
        rarity.update({product: cnt})
        cnt += 1
    return rarity

def classify_1(data, query_set):
    if data == 'trending':
        return query_set.annotate(num_owners=Count('owners')).order_by('-num_owners')
    elif data == 'rarity':
        return query_set.order_by('rarity')
    elif data == 'date-created-old':
        return query_set.order_by('created_at')
    elif data == 'date-created-new':
        return query_set.order_by('-created_at')
    elif data == 'price-highest':
        return query_set.order_by('-price')
    return query_set.order_by('price')

def add_search_data(view_func):
    def wrapper(request, *args, **kwargs):
        user_search = []
        for user in User.objects.filter(is_superuser=0).values():
            user_search.append({
                'id': str(user['id']),
                'name': user['name'],
                'image': user['avatar'],
                'redirect_url': 'profile'
            })

        product_search = []
        for product in NFTProduct.objects.values():
            product_search.append({
                'id': str(product['id']),
                'name': product['name'],
                'image': product['image'],
                'redirect_url': 'collection1'
            })

        blog_search = []
        for blog in NFTBlog.objects.values():
            blog_search.append({
                'id': str(blog['id']),
                'name': blog['title'],
                'image': blog['image'],
                'redirect_url': 'blog'
            })

        search_data = user_search + product_search + blog_search
        request.search_data = sorted(search_data, key=lambda x : x['name'])
        return view_func(request, *args, **kwargs)

    return wrapper