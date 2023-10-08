from math import ceil
import random
from django.shortcuts import render, HttpResponse
from NFTapp.models import User, NFTProduct, Topic, OwnerNFTProduct, Type, BlogSection, NFTBlog, Comment

def cal_times_to_read(blogs):
    blogs_context = {}
    for blog in blogs:
        words_of_blog = sum([len(str(section.content).split()) for section in blog.blog_section.all()])
        blogs_context[blog] = ceil(words_of_blog / average_wpm)
    return blogs_context

def home(request):
    context = {
        'hello': 'hellosss'
    }
    return render(request, 'NFTapp/home/home1.html', context)

def home2(request):
    context = {
        'hello': 'hellosss'
    }
    return render(request, 'NFTapp/home/home2.html', context)

def home5(request):
    context = {
        'hello': 'hellosss'
    }
    return render(request, 'NFTapp/home/home5.html', context)

def collection1(request):
    products = NFTProduct.objects.all()
    context = {
        "products": products
    }
    return render(request, 'NFTapp/explore/collection/collection1.html', context)

def collection2(request):
    products = NFTProduct.objects.all()
    context = {
        "products": products
    }
    return render(request, 'NFTapp/explore/collection/collection2.html', context)

def collection3(request):
    products = NFTProduct.objects.all()
    context = {
        "products": products
    }
    return render(request, 'NFTapp/explore/collection/collection3.html', context)

def collection4(request):
    products = NFTProduct.objects.all()
    context = {
        "products": products
    }
    return render(request, 'NFTapp/explore/collection/collection4.html', context)

def collection5(request):
    products = NFTProduct.objects.all()
    context = {
        "products": products
    }
    return render(request, 'NFTapp/explore/collection/collection5.html', context)

def FAQs1(request):
    return render(request, 'NFTapp/FAQs/FAQs1.html', {})

def FAQs2(request):
    return render(request, 'NFTapp/FAQs/FAQs2.html', {})

def FAQs3(request):
    return render(request, 'NFTapp/FAQs/FAQs3.html', {})

def FAQs4(request):
    return render(request, 'NFTapp/FAQs/FAQs4.html', {})

def FAQs5(request):
    return render(request, 'NFTapp/FAQs/FAQs5.html', {})

average_wpm = 238
blogs = NFTBlog.objects.all().order_by('image')
def blog(request):
    blogs_context = cal_times_to_read(blogs)
    # blogs = NFTBlog.objects.all().order_by('image')
    context = {
        'blogs': blogs_context
    }
    return render(request, 'NFTapp/blog/blog.html', context)

def blog_detail(request, pk):
    blog_detail = NFTBlog.objects.get(pk=pk)
    times_to_read = round(sum([len(str(section.content).split()) for section in blog_detail.blog_section.all()]) / average_wpm)
    random_blogs = list(blogs).copy()
    random_blogs.remove(blog_detail)
    blog_more_context = cal_times_to_read([random_blogs.pop(random.randint(0, len(random_blogs) - 1)) for i in range(3)])
    context = {
        'blog_detail': [blog_detail, times_to_read],
        'blog_more': blog_more_context
    }
    return render(request, 'NFTapp/blog/blog_detail.html', context)

