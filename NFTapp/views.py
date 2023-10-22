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
    blogs_context = {}
    for blog in blogs:
        words_of_blog = sum([len(str(section.content).split()) for section in blog.blog_section.all()])
        blogs_context[blog] = ceil(words_of_blog / average_wpm)
    return blogs_context

rarity = {}
def product_rarity():
    products = NFTProduct.objects.all().order_by('rarity')
    cnt = 1
    for product in products:
        rarity.update({product: cnt})
        cnt += 1

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


def home1(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title="Enjin")
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home1.html', context)

def home2(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title="Enjin")
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home2.html', context)

def home3(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title="Enjin")
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home3.html', context)

def home4(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title="Enjin")
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home4.html', context)

def home5(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title="Enjin")
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home5.html', context)

def collection1(request):
    products = NFTProduct.objects.all()
    data = request.GET.get('filter', 'trending')
    context = {
        "products": classify_1(request.GET.get('sort-by', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection1.html', context)

def collection_detail_1(request, pk):
    product = NFTProduct.objects.get(pk=pk)
    users = User.objects.filter(is_superuser=0)
    
    product_rarity()
    comments = product.product_comments.all().order_by('-added_at')
    # state = request.GET.get('state', None)
    # state_list = []
    # if state:
    #     state_list =  product.favorites_by.all() if state == 'favorite' else product.owners.all()
    product_favorite_list = product.favorites_by.all()
    product_owner_list = product.owners.all()
    user = User.objects.all();
    if request.method == 'POST':
        data = {
            "content": request.POST.get('content'),
            "vote": 0,
            "user": random.choice(user),
            "product": product,
        }
        product_comment = ProductComment.objects.create(**data)
        # return redirect('collection1', pk=product.id)
    context = {
        "product": product,
        "comments": comments,
        "rarity": rarity[product],
        "product_quantity": len(rarity),
        "product_favorite_list": product_favorite_list,
        'product_owner_list': product_owner_list,
    }
    return render(request, 'NFTapp/explore/nftproduct_detail.html', context)

def collection2(request):
    products = NFTProduct.objects.all()
    context = {
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection2.html', context)

def collection3(request):
    products = NFTProduct.objects.all()
    context = {
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection3.html', context)

def collection4(request):
    products = NFTProduct.objects.all()
    context = {
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection4.html', context)

def collection5(request):
    products = NFTProduct.objects.all()
    context = {
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection5.html', context)


def artworks1(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks1.html', context)

def artworks2(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': products.get(image='/static/images/explore/artworks/nft_image1.svg'),
    }
    return render(request, 'NFTapp/explore/artworks/artworks2.html', context)

def artworks3(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks3.html', context)

def artworks4(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks4.html', context)

def artworks5(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks5.html', context)


def about_us1(request):
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'products': products,
        'users': users,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/community/about_us/about_us1.html', context)

def about_us2(request):
    titles = FAQTitle.objects.all()
    users = User.objects.filter(is_superuser=0)
    context = {
        'titles': titles,
        'users': users,
    }
    return render(request, 'NFTapp/community/about_us/about_us2.html', context)

def about_us3(request):
    titles = FAQTitle.objects.all()
    users = User.objects.filter(is_superuser=0)
    context = {
        'titles': titles,
        'users': users,
    }
    return render(request, 'NFTapp/community/about_us/about_us3.html', context)


def about_us4(request):
    comments = []
    topic = "Alternate Medium Space"
    for product in NFTProduct.objects.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/community/about_us/about_us4.html', context)

def about_us5(request):
    return render(request, 'NFTapp/community/about_us/about_us5.html', {})

def artists(request):
    users = User.objects.filter(is_superuser=0)
    context = {
        'users': users
    } 
    return render(request, 'NFTapp/community/artists.html', context) 

def editorial(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.all()
    context = {
        'users': users,
        "products": products
    } 
    return render(request, 'NFTapp/community/editorial.html', context)

def FAQs1(request):
    titles = FAQTitle.objects.all()
    context = {
        'titles': titles
    }
    return render(request, 'NFTapp/community/FAQs/FAQs1.html', context)

def FAQs2(request):
    return render(request, 'NFTapp/community/FAQs/FAQs2.html', {})

def FAQs3(request):
    return render(request, 'NFTapp/community/FAQs/FAQs3.html', {})

def FAQs4(request):
    return render(request, 'NFTapp/community/FAQs/FAQs4.html', {})

def FAQs5(request):
    return render(request, 'NFTapp/community/FAQs/FAQs5.html', {})

average_wpm = 238
blogs = NFTBlog.objects.all().order_by('image')
def blog(request):
    blogs_context = cal_times_to_read(blogs)
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'blogs': blogs_context,
        'products': products,
        'users': users,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/blog/blog.html', context)

def blog_detail(request, pk):

    blog_detail = NFTBlog.objects.get(pk=pk)
    times_to_read = round(sum([len(str(section.content).split()) for section in blog_detail.blog_section.all()]) / average_wpm)
    random_blogs = list(blogs).copy()
    random_blogs.remove(blog_detail)
    blog_more_context = cal_times_to_read([random_blogs.pop(random.randint(0, len(random_blogs) - 1)) for i in range(3)])
    
    comments = blog_detail.blog_comments.all().order_by('-added_at')
    user = User.objects.all()
    if request.method == 'POST':
        data = {
            "vote": 0,
            "content": request.POST.get('content'),
            "user": random.choice(user), 
            "blog": blog_detail,
        }
        blog_comment = BlogComment.objects.create(**data)
    context = {
        'blog_detail': [blog_detail, times_to_read],
        'blog_more': blog_more_context,
        'comments': comments,
    }
    return render(request, 'NFTapp/blog/blog_detail.html', context)

def profile(request, pk):
    user = User.objects.get(pk=pk)
    context = {
        "user": user,
    }
    product_filter = request.GET.get('filter', 'collected')
    if product_filter == "collected":
        # product_collection = [product.product for product in user.owned_products.all()]
        product_collection = user.owners.all()
        context["products"] = product_collection
        # classify_1(request.GET.get('sort-by', 'trending'), product_collection)
    elif product_filter == "created":
        product_created = user.author.all()
        context["products"] = product_created 
        # classify_1(request.GET.get('sort-by', 'trending'), product_created)  
    else:
        product_favorited = user.favorites.all()
        context["products"] = product_favorited 
        # classify_1(request.GET.get('sort-by', 'trending'), product_favorited)
    return render(request, 'NFTapp/profile.html', context)

