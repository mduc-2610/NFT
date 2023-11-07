from collections import Counter
from math import ceil
import random, json
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .function import product_rarity_rank, classify_1, add_search_data, add_cart_data
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite, \
                                VoteProductComment, VoteBlogComment, \
                                DisvoteProductComment, DisvoteBlogComment, \
                                Follow, Cart, CartItem

from .forms import MyUserCreationForm, UserForm


def login_page(request):
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
    context = {
        'page': page,
    }
    return render(request, 'NFTapp/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home1')


def register_page(request):
    page = 'register'
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
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'NFTapp/login_register.html', context)
    
@login_required(login_url='login')
def edit_profile(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect ('profile', pk=request.user.id)
    return render(request, 'NFTapp/edit_profile.html', {'form': form})

@add_search_data
@add_cart_data
def home1(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    # cart_products = Cart.objects.get(user=request.user).products.all()

    # if request.method == 'POST':
    #     action = request.POST.get('action')
    #     if action == 'clear_cart_product':
    #         state = 'clear_cart_product'
    #         cart_products.delete()
    #         return JsonResponse({
    #             'state': state,
    #         })
    #     # elif action == 'delete_cart_product':
    #     #     state = "delete_cart_product"
    #     #     product_id = request.POST.get('product_id')
    #     #     Cart.objects.get(user=request.user).products.get(id=product_id).delete()
    #     #     return JsonResponse({
    #     #         'state': state
    #     #     })
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title='Enjin')
    comments = []
    topic = 'Alternate Medium Space'
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
        'blogs': blogs,
        'products': products,
        'users': users,
        'title': title,
        'comments': comments,
        'topic': topic,
        'search_data': request.search_data,
        'user__1': request.user,  
    }
    return render(request, 'NFTapp/home/home1.html', context)

@add_search_data
@add_cart_data
def home2(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title='Enjin')
    comments = []
    topic = 'Alternate Medium Space'
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
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
@add_cart_data
def home3(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title='Enjin')
    comments = []
    topic = 'Alternate Medium Space'
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
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
@add_cart_data
def home4(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title='Enjin')
    comments = []
    topic = 'Alternate Medium Space'
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
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
@add_cart_data
def home5(request):
    blogs = NFTBlog.objects.all()
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    title = FAQTitle.objects.get(title='Enjin')
    comments = []
    topic = 'Alternate Medium Space'
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
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
@add_cart_data
def collection1(request):
    products = NFTProduct.objects.all()
    data = request.GET.get('filter', 'trending')
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'products': classify_1(request.GET.get('sort-by', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection1.html', context)

@login_required(login_url='login')
@add_search_data
@add_cart_data
@csrf_exempt
def collection_detail_1(request, pk):
    product = NFTProduct.objects.get(pk=pk)
    users = User.objects.filter(is_superuser=0)    
    rarity_rank = product_rarity_rank()
    products = NFTProduct.objects.filter(type_product__name=product.type_product)
    product_list = list(products)
    comments = product.product_comments.all().order_by('-added_at')
    # product_comment_list = comments.product_comment_voted_by.all()
    product_favorite_list = product.favorites_by.all()
    product_owner_list = product.owned_by.all()
    user = User.objects.all();

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'comment':
            content = request.POST.get('content', None)
            valid_comment = True
            product_comment = None
            if content:
                data = {
                    'content': content,
                    'user': request.user,
                    'product': product,
                }
                product_comment = ProductComment.objects.create(**data)
            else:
                valid_comment = False
            
            context = {
                'valid_comment': valid_comment,
            }
            if valid_comment:
                context.update({'comment': serializers.serialize('json', [product_comment, request.user])})

            return JsonResponse(context)
        
        elif action == 'like':
            state = ""
            if request.user not in list(product.favorites.all()):
                NFTProductFavorite.objects.create(product=product, user=request.user)
                state = "like"
            else:
                NFTProductFavorite.objects.get(product=product, user=request.user).delete()
                state = "unlike"
            return JsonResponse({
                'state': state,
                'number_favorites': len(product.favorites.all()),
                'user_favorites': serializers.serialize('json', [request.user,])
            })
        
        elif action == 'list_follow':
            state = ""
            user_follow_id = request.POST.get('user_follow_id')
            user_target = User.objects.get(id=user_follow_id)
            request_user_following = request.user.following_set.all()
            if user_target not in [follow.followee for follow in request_user_following]: 
                Follow.objects.create(follower=request.user, followee=user_target)
                state = "follow"
            
            else:
                Follow.objects.get(follower=request.user, followee=user_target).delete()
                state = "unfollow"

            return JsonResponse({
                'state': state,
                'user_follow_id': user_follow_id, 
                'number_follow': len(request.user.following_set.all()),
                'user_follower': serializers.serialize("json", [user_target,]),
            })
        
        elif action == 'upvote': 
            state = ""
            state2 = ""
            comment_id = request.POST.get('comment_id') 
            comment = ProductComment.objects.get(id=comment_id)
            user_vote_list = list(comment.votes.all())
            if request.user not in user_vote_list:
                if DisvoteProductComment.objects.filter(user=request.user, comment=comment).exists():
                    DisvoteProductComment.objects.get(user=request.user, comment=comment).delete()
                    state2 = "deactivate_downvote"
                VoteProductComment.objects.create(user=request.user, comment=comment)
                state = "activate_upvote"
            else:
                VoteProductComment.objects.get(user=request.user, comment=comment).delete()
                state = "deactivate_upvote"

            return JsonResponse({
                'state': state,
                'state2': state2,
                'number_upvotes': len(comment.votes.all()),
                'number_downvotes': len(comment.disvotes.all()),
                'user_upvote': serializers.serialize('json', [request.user, ])
            })
        
        elif action == 'downvote': 
            state = ""
            state2 = ""
            comment_id = request.POST.get('comment_id') 
            comment = ProductComment.objects.get(id=comment_id)
            user_disvote_list = list(comment.disvotes.all())
            if request.user not in user_disvote_list:
                if VoteProductComment.objects.filter(user=request.user, comment=comment).exists():
                    VoteProductComment.objects.get(user=request.user, comment=comment).delete()
                    state2 = "deactivate_upvote"
                DisvoteProductComment.objects.create(user=request.user, comment=comment)
                state = "activate_downvote"
            else:
                DisvoteProductComment.objects.get(user=request.user, comment=comment).delete()
                state = "deactivate_downvote"

            return JsonResponse({
                'state': state,
                'state2': state,
                'number_upvotes': len(comment.votes.all()),
                'number_downvotes': len(comment.disvotes.all()),
                'user_downvote': serializers.serialize('json', [request.user, ])
            })

        elif action == 'cart_add':
            state = ""
            cart, _ = Cart.objects.get_or_create(user=request.user)
            if product not in [item.product for item in request.user.user_cart.cart_products.all()]:
                CartItem.objects.create(cart=cart, product=product)
                request.total_price += product.price;
                state = 'cart_add'
            else :
                CartItem.objects.get(cart=cart, product=product).delete()
                request.total_price -= product.price;
                state = 'cart_remove'
            return JsonResponse({
                'state': state,
                'total_price': request.total_price,
                'number_cart_products': len(request.user.user_cart.cart_products.all()),
                'product': serializers.serialize('json', [product, product.author, product.topic]),
            })


            # return redirect('collection1', pk=product.id)
    
    context = {
        'type_comment': 'product',
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'product': product,
        'comments': comments,
        'rarity_rank': rarity_rank[product],
        'product_quantity': len(rarity_rank),
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        # 'product_comment_list': product_comment_list, 
        'product_favorite_list': product_favorite_list,
        'product_owner_list': product_owner_list,
    }
    return render(request, 'NFTapp/explore/nftproduct_detail.html', context)

@add_search_data
@add_cart_data
def collection2(request):
    products = NFTProduct.objects.all()
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'products': classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection2.html', context)

@add_search_data
@add_cart_data
def collection3(request):
    products = NFTProduct.objects.all()
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'products': classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection3.html', context)

@add_search_data
@add_cart_data
def collection4(request):
    products = NFTProduct.objects.all()
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'products': classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection4.html', context)

@add_search_data
@add_cart_data
def collection5(request):
    products = NFTProduct.objects.all()
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'products': classify_1(request.GET.get('filter', 'trending'), products)
    }
    return render(request, 'NFTapp/explore/collection/collection5.html', context)


@add_search_data
@add_cart_data
def artworks1(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name='artworks')
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks1.html', context)

@add_search_data
@add_cart_data
def artworks2(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name='artworks')
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': NFTProduct.objects.get(image='/static/images/explore/artworks/nft_image1.svg'),
    }
    return render(request, 'NFTapp/explore/artworks/artworks2.html', context)

@add_search_data
@add_cart_data
def artworks3(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name='artworks')
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks3.html', context)

@add_search_data
@add_cart_data
def artworks4(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name='artworks')
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks4.html', context)

@add_search_data
@add_cart_data
def artworks5(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.filter(type_product__name='artworks')
    product_list = list(products)
    authors = []
    for user in users:
        if user.author.all().count():
            authors.append(user)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'authors': authors,
        'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        'users': users,
        'random_product': random.choice(products),
    }
    return render(request, 'NFTapp/explore/artworks/artworks5.html', context)


@add_search_data
@add_cart_data
def about_us1(request):
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    comments = []
    topic = 'Alternate Medium Space'
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'products': products,
        'users': users,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/community/about_us/about_us1.html', context)

@add_search_data
@add_cart_data
def about_us2(request):
    titles = FAQTitle.objects.all()
    users = User.objects.filter(is_superuser=0)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'titles': titles,
        'users': users,
    }
    return render(request, 'NFTapp/community/about_us/about_us2.html', context)

@add_search_data
@add_cart_data
def about_us3(request):
    titles = FAQTitle.objects.all()
    users = User.objects.filter(is_superuser=0)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'titles': titles,
        'users': users,
    }
    return render(request, 'NFTapp/community/about_us/about_us3.html', context)


@add_search_data
@add_cart_data
def about_us4(request):
    comments = []
    topic = 'Alternate Medium Space'
    for product in NFTProduct.objects.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/community/about_us/about_us4.html', context)

@add_search_data
@add_cart_data
def about_us5(request):
    return render(request, 'NFTapp/community/about_us/about_us5.html', {})

@add_search_data
@add_cart_data
def artists(request):
    users = User.objects.filter(is_superuser=0).annotate(num_products=Count('owners')).order_by('-num_products')
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'users': users
    } 
    return render(request, 'NFTapp/community/artists.html', context) 

@add_search_data
@add_cart_data
def editorial(request):
    users = User.objects.filter(is_superuser=0)
    products = NFTProduct.objects.all()
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'users': users,
        'products': products
    } 
    return render(request, 'NFTapp/community/editorial.html', context)

@add_search_data
@add_cart_data
def FAQs1(request):
    titles = FAQTitle.objects.all()
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'titles': titles
    }
    return render(request, 'NFTapp/community/FAQs/FAQs1.html', context)

@add_search_data
@add_cart_data
def FAQs2(request):
    return render(request, 'NFTapp/community/FAQs/FAQs2.html', {})

@add_search_data
@add_cart_data
def FAQs3(request):
    return render(request, 'NFTapp/community/FAQs/FAQs3.html', {})

@add_search_data
@add_cart_data
def FAQs4(request):
    return render(request, 'NFTapp/community/FAQs/FAQs4.html', {})

@add_search_data
@add_cart_data
def FAQs5(request):
    return render(request, 'NFTapp/community/FAQs/FAQs5.html', {})


@add_search_data
@add_cart_data
def blog(request):
    blogs = NFTBlog.objects.all().order_by('image')
    products = NFTProduct.objects.all()
    users = User.objects.filter(is_superuser=0)
    comments = []
    topic = 'Alternate Medium Space'
    for product in products.filter(topic__name=topic):
        for comment in product.product_comments.all():      
            comments.append(comment)
    context = {
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'blogs': blogs,
        'products': products,
        'users': users,
        'comments': comments,
        'topic': topic
    }
    return render(request, 'NFTapp/blog/blog.html', context)

average_wpm = 238
@login_required(login_url='/login')
@add_search_data
@add_cart_data
def blog_detail(request, pk):
    blogs = NFTBlog.objects.all()
    blog_detail = NFTBlog.objects.get(pk=pk)
    times_to_read = round(sum([len(str(section.content).split()) for section in blog_detail.blog_section.all()]) / average_wpm)
    random_blogs = list(blogs).copy()
    random_blogs.remove(blog_detail)
    blogs_more = [random_blogs.pop(random.randint(0, len(random_blogs) - 1)) for i in range(3)]
    
    comments = blog_detail.blog_comments.all().order_by('-added_at')
    user = User.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action', None)
        
        if action == 'comment':
            content = request.POST.get('content', None)
            valid_comment = True
            blog_comment = None
            if content:
                data = {
                    'content': content,
                    'user': request.user,
                    'blog': blog_detail,
                }
                blog_comment = BlogComment.objects.create(**data)
            else:
                valid_comment = False
            
            context = {
                'valid_comment': valid_comment,
            }
            if valid_comment:
                context.update({'comment': serializers.serialize('json', [blog_comment, request.user])})

            return JsonResponse(context)
        
        if action == 'upvote': 
            state = ""
            state2 = ""
            comment_id = request.POST.get('comment_id') 
            comment = BlogComment.objects.get(id=comment_id)
            user_vote_list = list(comment.votes.all())
            if request.user not in user_vote_list:
                if DisvoteBlogComment.objects.filter(user=request.user, comment=comment).exists():
                    DisvoteBlogComment.objects.get(user=request.user, comment=comment).delete()
                    state2 = "deactivate_downvote"
                VoteBlogComment.objects.create(user=request.user, comment=comment)
                state = "activate_upvote"
            else:
                VoteBlogComment.objects.get(user=request.user, comment=comment).delete()
                state = "deactivate_upvote"

            return JsonResponse({
                'state': state,
                'state2': state2,
                'number_upvotes': len(comment.votes.all()),
                'number_downvotes': len(comment.disvotes.all()),
                'user_upvote': serializers.serialize('json', [request.user, ])
            })
        
        elif action == 'downvote': 
            state = ""
            state2 = ""
            comment_id = request.POST.get('comment_id') 
            comment = BlogComment.objects.get(id=comment_id)
            user_disvote_list = list(comment.disvotes.all())
            if request.user not in user_disvote_list:
                if VoteBlogComment.objects.filter(user=request.user, comment=comment).exists():
                    VoteBlogComment.objects.get(user=request.user, comment=comment).delete()
                    state2 = "deactivate_upvote"
                DisvoteBlogComment.objects.create(user=request.user, comment=comment)
                state = "activate_downvote"
            else:
                DisvoteBlogComment.objects.get(user=request.user, comment=comment).delete()
                state = "deactivate_downvote"

            return JsonResponse({
                'state': state,
                'state2': state,
                'number_upvotes': len(comment.votes.all()),
                'number_downvotes': len(comment.disvotes.all()),
                'user_downvote': serializers.serialize('json', [request.user, ])
            })
        
        elif action == 'list_follow':
            state = ""
            user_follow_id = request.POST.get('user_follow_id')
            user_target = User.objects.get(id=user_follow_id)
            request_user_following = request.user.following_set.all()
            if user_target not in [follow.followee for follow in request_user_following]: 
                Follow.objects.create(follower=request.user, followee=user_target)
                state = "follow"
            
            else:
                Follow.objects.get(follower=request.user, followee=user_target).delete()
                state = "unfollow"

            return JsonResponse({
                'state': state,
                'user_follow_id': user_follow_id, 
                'number_follow': len(request.user.following_set.all()),
                'user_follower': serializers.serialize("json", [user_target,]),
            })
        
    context = {
        'type_comment': 'blog',
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'blog_detail': [blog_detail, times_to_read],
        'blogs': blogs_more,
        'comments': comments,
    }
    return render(request, 'NFTapp/blog/blog_detail.html', context)

@csrf_exempt
@add_search_data
@add_cart_data
def profile(request, pk):
    user = User.objects.get(pk=pk)
    profile_user_follower = user.follower_set.all()
    profile_user_followee = user.following_set.all()
    product_filter = request.GET.get('filter', 'collected')
    context = {}
    if product_filter == 'collected':
        # product_collection = [product.product for product in user.owned_products.all()]
        product_collection = user.owners.all()
        context['products'] = product_collection
        # classify_1(request.GET.get('sort-by', 'trending'), product_collection)
    elif product_filter == 'created':
        product_created = user.author.all()
        context['products'] = product_created 
        # classify_1(request.GET.get('sort-by', 'trending'), product_created)  
    else:
        product_favorited = user.favorites.all()
        context['products'] = product_favorited 
        # classify_1(request.GET.get('sort-by', 'trending'), product_favorited)

    # total_price = sum([product.price for product in Cart.objects.get(user=request.user).products.all()])
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'search_product':
            state = ''
            products_found, additional_fields = [], []
            search_query = request.POST.get('search_data', None)
            if search_query:
                product_query = context['products'].filter(
                    Q(name__istartswith=search_query) |
                    Q(topic__name__istartswith=search_query)
                )    
            
                if product_query.exists():
                    for product in product_query:
                        products_found.append(product)
                        additional = {
                            'topic_name': product.topic.name,
                            'owned': True if product in request.user.owners.all() or product.author == request.user else False,
                            'in_cart': True if product in request.user.user_cart.products.all()  else False,
                        }
                        additional_fields.append(additional)
                    state = 'found'
                else:
                    state = 'not_found'
            
            context = {
                'search_query': search_query,
                'state': state,
                'user': serializers.serialize('json', [request.user, ])
            }  
            if state == 'found':
                context.update({
                    'products_found': serializers.serialize('json', products_found),
                    'additional_fields': json.dumps(additional_fields),
                    'num_products': len(products_found)
                })
            return JsonResponse(context, safe=False)
            
        if action == 'follow':
            state = ""
            user_follow_id = request.POST.get('user_follow_id')
            request_user_following = request.user.following_set.all()
            request_user_follow = None
            if user not in [follow.followee for follow in request_user_following]: 
                request_user_follow = Follow.objects.create(follower=request.user, followee=user)
                # request_user_following.add(user)
                state = "follow"
            else:
                request_user_follow = Follow.objects.get(follower=request.user, followee=user)
                Follow.objects.get(follower=request.user, followee=user).delete()
                # request_user_following.remove(user)
                state = "unfollow"
            return JsonResponse({
                    'state': state,
                    'user_follow_id': user_follow_id,
                    'number_follower': len(user.follower_set.all()),
                    'profile_user_follower': serializers.serialize("json", [request_user_follow.follower,]),
                })
        # elif action == 'list_follow':
        #     state = ""
        #     user_follow_id = request.POST.get('user_follow_id')
        #     user_target = User.objects.get(id=user_follow_id)
        #     request_user_following = request.user.following_set.all()
        #     if user_target not in [follow.followee for follow in request_user_following]: 
        #         Follow.objects.create(follower=request.user, followee=user_target)
        #         state = "follow"
        #     else:
        #         # request_user_follow = Follow.objects.get(follower=request.user, followee=user_target)
        #         Follow.objects.get(follower=request.user, followee=user_target).delete()
        #         state = "unfollow"
        #     return JsonResponse({
        #             'state': state,
        #             'user_follow_id': user_follow_id, 
        #             'number_follow': len(request.user.following_set.all()),
        #             'user_position': serializers.serialize("json", [user,]),
        #             'profile_user_follower': serializers.serialize("json", [user_target,]),
        #         })
        
        elif action == 'list_follow':
            state = ""
            user_follow_id = request.POST.get('user_follow_id')
            user_target = User.objects.get(id=user_follow_id)
            request_user_following = request.user.following_set.all()
            if user_target not in [follow.followee for follow in request_user_following]: 
                Follow.objects.create(follower=request.user, followee=user_target)
                state = "follow"
            
            else:
                Follow.objects.get(follower=request.user, followee=user_target).delete()
                state = "unfollow"

            return JsonResponse({
                'state': state,
                'user_follow_id': user_follow_id, 
                'number_follow': len(request.user.following_set.all()),
                'user_follower': serializers.serialize("json", [user_target,]),
            })
        
        elif action == 'cart_add':
            state = ""
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product_id = request.POST.get('product_id')
            product = NFTProduct.objects.get(id=product_id)
            if product not in [item.product for item in request.user.user_cart.cart_products.all()]:
                CartItem.objects.create(cart=cart, product=product)
                request.total_price += product.price
                state = 'cart_add'
            else :
                CartItem.objects.get(cart=cart, product=product).delete()
                request.total_price -= product.price
                state = 'cart_remove'
                
            return JsonResponse({
                'state': state,
                'total_price': request.total_price,
                'number_cart_products': len(request.user.user_cart.cart_products.all()),
                'product': serializers.serialize('json', [product, product.author, product.topic]),
            })

    context.update({
        'cart_products': request.cart_products,
        'search_data': request.search_data,
        'user': user,
        'profile_user_follower': profile_user_follower,
        'profile_user_followee': profile_user_followee,
    })
    return render(request, 'NFTapp/profile.html', context)

@add_search_data
@add_cart_data
def search_result(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', None)
        if search_query:
            product_query = NFTProduct.objects.filter(
                Q(name__istartswith=search_query) 
                # Q(topic__name__istartswith=search_query) 
                # Q(description__istartswith=search_query) 
                # Q(quantity=search_query) |
                # Q(rarity=search_query)
            )
            blog_query = NFTBlog.objects.filter(
                Q(title__istartswith=search_query) 
                # Q(author__name__istartswith=search_query)
            )
            
            user_query = User.objects.filter(
                Q(name__istartswith=search_query) 
                # Q(bio__istartswith=search_query) |
                # Q(property__istartswith=search_query)     
            )

        query_type = [product_query, blog_query, user_query]
        redirect_page = ['collection1', 'blog', 'profile']
        valid_query = []
        mapping = {}
        for index, query in enumerate(query_type):
            if query.exists():
                valid_query.append(query)              
                mapping[query] = redirect_page[index] 
                
        if  len(valid_query) == 1 and len(valid_query[0]) == 1:
                return redirect(mapping[valid_query[0]], pk=valid_query[0][0].id) 
        
        context = {
            'search_data': request.search_data,                
            'cart_products': request.cart_products,
        }
        
        if len(valid_query) != 0:
            context.update({
                'search_query': search_query,
                'valid_query': valid_query,
                'products': product_query,
                'users': user_query,
                'blogs': blog_query,  
            })
        else:
            context.update({
                'bad_query': 'No results found'
            })
        return render(request, 'NFTapp/search_result.html', context)