from collections import Counter
from math import ceil
import random
from . import views
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.db.models import Count, Q, Sum
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite, \
                                Cart, CartItem, TradeHistory
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.db.models.functions import Extract
from datetime import date, datetime, timedelta

def error_403_csrf_failure(request, reason=""):
    """
    To fix this issue:
        1. User opens tab A and tab B, and both show the login in form.
        2. User logs in on tab A, this will destroy the Anonymous session, and create a new one (for security)
        3. Then user logs in on tab B
            - The CSRF token for the Anonymous session is now invalid
            - Since the user is already logged, we just redirect them to refresh the page
    """
    if request.path == '/login/' and request.user.is_authenticated:
        next = request.GET.get('next', '/')
        return HttpResponseRedirect(next)

    url = reverse('login') + '?next=' + request.path
    context = {
        'page_title': "Authentication Error",
        'continue_url': url,
        'reason': reason,
    }
    response = render(request, "core.base/403_csrf.html", context=context)
    response.status_code = 403
    return response

def product_rarity_rank():
    rarity_rank = {}
    products = NFTProduct.objects.all().order_by('rarity')
    cnt = 1
    for product in products:
        rarity_rank.update({product: cnt})
        cnt += 1
    return rarity_rank

def classify_1(data, query_set):
    if data == 'trending':
        return query_set.annotate(num_owners=Count('owners')).order_by('-num_owners')
    elif data == 'rarity':
        return query_set.order_by('rarity')
    elif data == 'date-created-new':
        return query_set.order_by('-created_at')
    elif data == 'date-created-old':
        return query_set.order_by('created_at')
    elif data == 'price-highest':
        return query_set.order_by('-price')
    return query_set.order_by('price')

def classify_3(data, query_set):
    if data == 'all':
        return query_set
    elif data == 'today':
        return query_set.filter(created_at__date=date.today())
    elif data == 'last-week':
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_last_week = start_of_week - timedelta(days=7)
        end_of_last_week = start_of_last_week + timedelta(days=6)

        filtered_records = query_set.filter(
            created_at__date__gte=start_of_last_week,
            created_at__date__lte=end_of_last_week
        )
        return filtered_records
    else:
        current_date = datetime.now().date()

        start_of_last_month = current_date.replace(day=1) - timedelta(days=1)

        end_of_last_month = current_date.replace(day=1) - timedelta(days=1)

        filtered_records = query_set.filter(
            created_at__date__gte=start_of_last_month,
            created_at__date__lte=end_of_last_month
        )

        return filtered_records
    
def artists_classify(data, query_set):
    if data == 'follower':
        return query_set.annotate(num_followers=Count('follower_set')).order_by('-num_followers')
    elif data == 'unique-collectors':
        return query_set.annotate(num_owners=Count('owners')).order_by('-num_owners')
    elif data == 'created':
        return query_set.annotate(num_created=Count('author')).order_by('-num_created')
    elif data == 'nft-sold':
        query_set = list(query_set)
        return sorted(query_set, key=lambda x : -x.sold())
    return query_set.order_by('-property')


def add_cart_data(view_func):
    def wrapper(request, *args, **kwargs):
        request.cart_products = None
        if request.user.is_authenticated:
            cart_products = []
            user_owned_products = request.user.owners.all()
            for product in Cart.objects.get(user=request.user).products.all():
                if product not in user_owned_products:
                    cart_products.append(product)

            cart_products_length = len(cart_products)
            total_price = sum([product.price for product in cart_products])
            request.number_cart_products = cart_products
            if request.method == 'POST':
                action = request.POST.get('action')
                if action == 'clear_cart_product':
                    state = 'clear_cart_product'
                    request.user.user_cart.cart_products.all().delete()
                    return JsonResponse({
                        'state': state,
                    })
                
                elif action == 'delete_cart_product':
                    state = "delete_cart_product"
                    product_id = request.POST.get('product_id')
                    product_delete = NFTProduct.objects.get(id=product_id)
                    user_cart = Cart.objects.get(user=request.user)
                    CartItem.objects.get(cart=user_cart, product=product_delete).delete()
                    cart_products_length -= 1
                    total_price -= product_delete.price

                    return JsonResponse({
                        'state': state,
                        'total_price': total_price,
                        'number_cart_products': cart_products_length,
                        'product_delete': serializers.serialize('json', [product_delete, ]),
                    })
                
                elif action == 'purchase_cart_product':
                    state = ""
                    cart_products = request.user.user_cart.products.all()
                    context = {}
                    if total_price <= request.user.property:
                        cart_products_buyed = cart_products
                        # for product in cart_products:
                        #     request.user.owners.add(product)
                        #     request.user.user_cart.products.remove(product)
                        #     product.quantity -= 1
                        #     product.save()

                        #     TradeHistory.objects.create(
                        #         buyer=request.user,
                        #         seller=product.author,
                        #         product=product,
                        #         price_at_purchase=product.price,
                        #         quantity_at_purchase=product.quantity
                        #     )
                            
                        # request.user.property -= total_price
                        # request.user.save()
                        state = 'can_buy'
                        context = {
                            'state': 'can_buy',
                            'cart_products_buyed': serializers.serialize('json', list(cart_products_buyed))
                        }
                    else:
                        state = 'cant_buy'
                        context = {'state': 'cant_buy'}
                    context['user'] = serializers.serialize('json', [request.user, ])
                    return JsonResponse(context)

            request.total_price = total_price    
            request.cart_products = cart_products
        return view_func(request, *args, **kwargs)
    
    return wrapper

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