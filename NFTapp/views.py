from math import ceil
from django.shortcuts import render, HttpResponse
from NFTapp.models import User, NFTProduct, Topic, OwnerNFTProduct, Type, BlogSection, NFTBlog, Comment


# Create your views here.
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

blogs_context = {}
def blog(request):
    blogs = NFTBlog.objects.all().order_by('image')
    average_wpm = 238
    for blog in blogs:
        words_of_blog = sum([len(str(section.content).split()) for section in blog.blog_section.all()])
        blogs_context[blog] = ceil(words_of_blog / average_wpm)
    context = {
        'blogs': blogs_context
    }
    return render(request, 'NFTapp/blog/blog.html', context)

def blog_detail(request, pk):
    blog_detail = NFTBlog.objects.get(pk=pk)
    context = {
        'blog': [blog_detail, blogs_context[blog_detail]]
    }
    return render(request, 'NFTapp/blog/blog_detail.html', context)