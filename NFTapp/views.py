from collections import Counter
from math import ceil
import random, json
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .function import cal_times_to_read, product_rarity_rank, classify_1, add_search_data
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite
from .forms import MyUserCreationForm
from django.db.models import Count


def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home1')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')  # Redirect to login page on failure

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home1')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    context = {'page': page}
    return render(request, 'NFTapp/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home1')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home1')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'NFTapp/login_register.html', {'form': form})

@add_search_data
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
        'topic': topic,
        'search_data': request.search_data,
        'user__1': request.user 
    }
    return render(request, 'NFTapp/home/home1.html', context)

@add_search_data
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
        'topic': topic,
        'search_data': request.search_data 
    }
    return render(request, 'NFTapp/home/home2.html', context)

@add_search_data
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
        'search_data': request.search_data,
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home3.html', context)


@add_search_data
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
        'search_data': request.search_data,
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home4.html', context)


@add_search_data
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
        'search_data': request.search_data,
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/home/home5.html', context)

@add_search_data
def collection1(request):
    products = NFTProduct.objects.all()
    data = request.GET.get('filter', 'trending')
    context = {
        'search_data': request.search_data,
        "products": classify_1(request.GET.get('sort-by', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection1.html', context)

@login_required(login_url='login')
@add_search_data
def collection_detail_1(request, pk):
    product = NFTProduct.objects.get(pk=pk)
    users = User.objects.filter(is_superuser=0)    
    rarity_rank = product_rarity_rank()
    comments = product.product_comments.all().order_by('-added_at')
    product_favorite_list = product.favorites_by.all()
    product_owner_list = product.owners.all()
    user = User.objects.all();
    
    like = False
    if NFTProductFavorite.objects.filter(user=request.user, product=product).exists():
        like = True

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'like':
            data = {
                'user': request.user,
                'product': product
            }
            product_favorite_by = NFTProductFavorite.objects.filter(user=request.user, product=product)
            if product_favorite_by.exists():
                product_favorite_by.delete()
                like = False
            else:
                product_favorite_by = NFTProductFavorite.objects.create(**data)
                like = True
                
        elif action == 'comment':
            data = {
                "content": request.POST.get('content'),
                "vote": 0,
                "user": request.user,
                "product": product,
            }
            product_comment = ProductComment.objects.create(**data)
            # return redirect('collection1', pk=product.id)
    context = {
        'search_data': request.search_data,
        "product": product,
        "comments": comments,
        "rarity_rank": rarity_rank[product],
        "product_quantity": len(rarity_rank),
        "product_favorite_list": product_favorite_list,
        'product_owner_list': product_owner_list,
        'like': like,
    }
    return render(request, 'NFTapp/explore/nftproduct_detail.html', context)

@add_search_data
def collection2(request):
    products = NFTProduct.objects.all()
    context = {
        'search_data': request.search_data,
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection2.html', context)

@add_search_data
def collection3(request):
    products = NFTProduct.objects.all()
    context = {
        'search_data': request.search_data,
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection3.html', context)

@add_search_data
def collection4(request):
    products = NFTProduct.objects.all()
    context = {
        'search_data': request.search_data,
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection4.html', context)

@add_search_data
def collection5(request):
    products = NFTProduct.objects.all()
    context = {
        'search_data': request.search_data,
        "products": classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection5.html', context)


@add_search_data
def artworks1(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks1.html', context)

@add_search_data
def artworks2(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': NFTProduct.objects.get(image='/static/images/explore/artworks/nft_image1.svg'),
    }
    return render(request, 'NFTapp/explore/artworks/artworks2.html', context)

@add_search_data
def artworks3(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks3.html', context)

@add_search_data
def artworks4(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks4.html', context)

@add_search_data
def artworks5(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name="artworks")
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks5.html', context)


@add_search_data
def about_us1(request):
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    comments = []
    topic = "Alternate Medium Space"
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'search_data': request.search_data,
        'products': products,
        'users': users,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/community/about_us/about_us1.html', context)

@add_search_data
def about_us2(request):
    titles = FAQTitle.objects.all()
    users = User.objects.filter(is_superuser=0)
    context = {
        'search_data': request.search_data,
        'titles': titles,
        'users': users,
    }
    return render(request, 'NFTapp/community/about_us/about_us2.html', context)

@add_search_data
def about_us3(request):
    titles = FAQTitle.objects.all()
    users = User.objects.filter(is_superuser=0)
    context = {
        'search_data': request.search_data,
        'titles': titles,
        'users': users,
    }
    return render(request, 'NFTapp/community/about_us/about_us3.html', context)


@add_search_data
def about_us4(request):
    comments = []
    topic = "Alternate Medium Space"
    for product in NFTProduct.objects.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'search_data': request.search_data,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/community/about_us/about_us4.html', context)

@add_search_data
def about_us5(request):
    return render(request, 'NFTapp/community/about_us/about_us5.html', {})

@add_search_data
def artists(request):
    users = User.objects.filter(is_superuser=0).annotate(num_products=Count('owners')).order_by('-num_products')
    context = {
        'search_data': request.search_data,
        'users': users
    } 
    return render(request, 'NFTapp/community/artists.html', context) 

@add_search_data
def editorial(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.all()
    context = {
        'search_data': request.search_data,
        'users': users,
        "products": products
    } 
    return render(request, 'NFTapp/community/editorial.html', context)

@add_search_data
def FAQs1(request):
    titles = FAQTitle.objects.all()
    context = {
        'search_data': request.search_data,
        'titles': titles
    }
    return render(request, 'NFTapp/community/FAQs/FAQs1.html', context)

@add_search_data
def FAQs2(request):
    return render(request, 'NFTapp/community/FAQs/FAQs2.html', {})

@add_search_data
def FAQs3(request):
    return render(request, 'NFTapp/community/FAQs/FAQs3.html', {})

@add_search_data
def FAQs4(request):
    return render(request, 'NFTapp/community/FAQs/FAQs4.html', {})

@add_search_data
def FAQs5(request):
    return render(request, 'NFTapp/community/FAQs/FAQs5.html', {})


blogs = NFTBlog.objects.all().order_by('image')
@add_search_data
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
        'search_data': request.search_data,
        'blogs': blogs_context,
        'products': products,
        'users': users,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/blog/blog.html', context)

average_wpm = 238
@add_search_data
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
        'search_data': request.search_data,
        'blog_detail': [blog_detail, times_to_read],
        'blog_more': blog_more_context,
        'comments': comments,
    }
    return render(request, 'NFTapp/blog/blog_detail.html', context)

@add_search_data
def profile(request, pk):
    user = User.objects.get(pk=pk)
    context = {
        'search_data': request.search_data,
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

