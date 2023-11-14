from collections import Counter
from math import ceil
import random, json
from decimal import Decimal

from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.views import View
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator

from .functions import product_rarity_rank, classify_1, classify_3, artists_classify, add_search_data, add_cart_data
from .forms import MyUserCreationForm, UserForm
from .models import User, NFTProduct, Topic,\
                    NFTProductOwner, Type, NFTBlog, \
                    BlogSection, FAQ, FAQTitle,\
                    BlogComment, ProductComment, NFTProductFavorite, \
                    VoteProductComment, VoteBlogComment, \
                    DisvoteProductComment, DisvoteBlogComment, \
                    Follow, Cart, CartItem, TradeHistory

class LoginView(View):
    template_name = 'NFTapp/login_register.html'

    def get(self, request, *args, **kwargs):
        page = 'login'
        if request.user.is_authenticated:
            return redirect('home1')
        context = {
            'page': page
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('login')  
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home1')
        else:
            messages.error(request, 'Username or password is incorrect')

        context = {'page': 'login'}
        return render(request, self.template_name, context)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home1')

class RegisterView(View):
    template_name = 'NFTapp/login_register.html'

    def get(self, request, *args, **kwargs):
        page = 'register'
        form = MyUserCreationForm()
        context = {
            'page': page,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        page = 'register'
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.property = random.uniform(0, 20)
            user.save()
            Cart.objects.create(user=user)
            login(request, user)
            return redirect('home1')
        else:
            messages.error(request, 'An error occurred during registration')

        context = {'page': page, 'form': form}
        return render(request, self.template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'NFTapp/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form = UserForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=request.user.id)

        return render(request, self.template_name, {'form': form})
    
    
@method_decorator(csrf_exempt, name='dispatch')    
@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class ProfileView(LoginRequiredMixin, View):
    template_name = 'NFTapp/profile.html'
    login_url = '/login/'

    def get_context_data(self, pk):
        user = get_object_or_404(User, pk=pk)
        profile_user_follower = user.follower_set.all()
        profile_user_followee = user.following_set.all()
        product_filter = self.request.GET.get('filter', 'collected')
        context = {}
        product_collected = user.owners.all()
        product_created = user.author.all()
        product_favorited = user.favorites.all()

        context['products_collected_len'] = len(product_collected)
        context['products_created_len'] = len(product_created)
        context['products_favorited_len'] = len(product_favorited)

        if product_filter == 'collected':
            context['products'] = product_collected
        elif product_filter == 'created':
            context['products'] = product_created
        else:
            context['products'] = product_favorited

        context.update({
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'user': user,
            'profile_user_follower': profile_user_follower,
            'profile_user_followee': profile_user_followee,
        })
        return context

    def get(self, request, pk):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        context = self.get_context_data(pk)
        user = context['user']
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
            
            context_json = {
                'search_query': search_query,
                'state': state,
                'user': serializers.serialize('json', [request.user, ])
            }  
            if state == 'found':
                context_json.update({
                    'products_found': serializers.serialize('json', products_found),
                    'additional_fields': json.dumps(additional_fields),
                    'num_products': len(products_found)
                })
            return JsonResponse(context_json, safe=False)
        
        elif action == 'filter_product':
            filter_data = request.POST.get('filter_data', None)
            products_filter, additional_fields = [], []
            type_filter = ''
            if filter_data is not None:
                if filter_data == 'trending':
                    products = context['products'].annotate(num_owners=Count('owners')).order_by('-num_owners')
                    type_filter = 'Trending'
                elif filter_data == 'rarity':
                    products = context['products'].order_by('rarity')
                    type_filter = 'Rarity'
                elif filter_data == 'date-created-new':
                    products = context['products'].order_by('-created_at')
                    type_filter = 'Date created - Newest'
                elif filter_data == 'date-created-old':
                    products = context['products'].order_by('created_at')
                    type_filter = 'Date created - Oldest'
                elif filter_data == 'price-highest':
                    products = context['products'].order_by('-price')
                    type_filter = 'Price - highest'
                else:
                    products = context['products'].order_by('price')
                    type_filter = 'Price - lowest'

                context_json = {
                    'type_filter': type_filter
                }
                if products_filter is not None:
                    for product in products:
                        products_filter.append(product)
                        additional = {
                            'topic_name': product.topic.name,
                            'owned': True if product in request.user.owners.all() or product.author == request.user else False,
                            'in_cart': True if product in request.user.user_cart.products.all()  else False,
                        }
                        additional_fields.append(additional)
                        
                    context_json.update({
                        'state': 'found',
                        'num_products': len(products_filter),
                        'user': serializers.serialize('json', [request.user, ]),
                        'additional_fields': json.dumps(additional_fields),
                        'products_filter': serializers.serialize('json', products_filter),
                    })
                else:
                    context_json.update({
                        'state': 'not_found'
                    })
                return JsonResponse(context_json, safe=False)
        
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

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class TradeHistoryView(LoginRequiredMixin, View):
    template_name = 'NFTapp/trade_history.html'

    def get_context_data(self, request):
        trades = request.user.buyer_trades.all()
        context = {
            'page': 'trade_history',
            'trades': trades,
            'search_data': request.search_data,
        }
        return context

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get('action')
        context = {}

        if action == 'search_product':
            state = ''
            trades_found = []
            search_query = request.POST.get('search_data', None)
            search_query = search_query.lower()

            if search_query:
                for trade in request.user.buyer_trades.all():
                    if (
                        trade.product.name.lower().startswith(search_query.lower())
                        or str(trade.timestamp.year).lower().startswith(search_query)
                        or str(trade.timestamp.month).lower().startswith(search_query)
                        or str(trade.timestamp.day).lower().startswith(search_query)
                    ):
                        product = NFTProduct.objects.get(pk=trade.product.id)
                        seller = User.objects.get(pk=product.author.id)
                        trades_found.append(
                            {
                                'trade_id': str(trade.id),
                                'buyer_name': request.user.name,
                                'buyer_id': str(request.user.id),
                                'seller_name': seller.name,
                                'seller_id': str(seller.id),
                                'product_id': str(product.id),
                                'product_name': product.name,
                                'product_price': str(product.price),
                                'price_at_purchase': str(trade.price_at_purchase),
                                'quantity_at_purchase': str(trade.quantity_at_purchase),
                                'timestamp': str(trade.timestamp),
                            }
                        )
                if len(trades_found):
                    state = 'found'
                else:
                    state = 'not_found'

            context_json = {'search_query': search_query, 'state': state}

            if state == 'found':
                context_json.update({'trades_found': json.dumps(trades_found)})

            return JsonResponse(context_json, safe=False)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class SearchResultView(View):
    template_name = 'NFTapp/search_result.html'

    def post(self, request, *args, **kwargs):
        search_query = self.request.POST.get('search_query', None)

        if search_query:
            product_query = NFTProduct.objects.filter(
                Q(name__istartswith=search_query) |
                Q(topic__name__istartswith=search_query)
                # Q(description__istartswith=search_query)
                # Q(quantity=search_query) |
                # Q(rarity=search_query)
            )
            blog_query = NFTBlog.objects.filter(
                Q(title__istartswith=search_query) |
                Q(author__name__istartswith=search_query)
            )

            user_query = User.objects.filter(
                Q(name__istartswith=search_query)
                # Q(property__istartswith=search_query)
                # Q(bio__istartswith=search_query) |
            )

            query_type = [product_query, blog_query, user_query]
            redirect_page = ['collection1', 'blog', 'profile']
            valid_query = []
            mapping = {}
            for index, query in enumerate(query_type):
                if query.exists():
                    valid_query.append(query)
                    mapping[query] = redirect_page[index]

            if len(valid_query) == 1 and len(valid_query[0]) == 1:
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
            return render(request, self.template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class HomeView(View):
    template_name = 'NFTapp/home/home{}.html'

    def get_context_data(self):
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
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'blogs': blogs,
            'products': products,
            'users': users,
            'title': title,
            'comments': comments,
            'topic': topic,
        }

        return context

    def get(self, request, num):
        context = self.get_context_data()
        template_name = self.template_name.format(num)
        return render(request, template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class CollectionView(View):
    template_name = 'NFTapp/explore/collection/collection{}.html'

    def get_context_data(self, classify_feature, classify_data):
        products = NFTProduct.objects.all()
        sort_data = classify_data
        sort_type = ' '.join([x.title() for x in sort_data.split('-')])
        context = {
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'products': classify_feature(sort_data, products),
            'sort_type': sort_type
        }
        return context

    def get(self, request, num, classify_feature):
        context = self.get_context_data(classify_feature, request.GET.get('sort-by', 'trending'))
        template_name = self.template_name.format(num)
        return render(request, template_name, context)


@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class CollectionDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'NFTapp/explore/nftproduct_detail.html'

    def get_context_data(self, pk):
        product = NFTProduct.objects.get(pk=pk)
        users = User.objects.filter(is_superuser=0)    
        rarity_rank = product_rarity_rank()
        products = NFTProduct.objects.filter(type_product__name=product.type_product)
        product_list = list(products)
        comments = product.product_comments.all()
        product_favorite_list = product.favorites_by.all()
        product_owner_list = product.owned_by.all()

        context = {
            'type_comment': 'product',
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'product': product,
            'comments': comments,
            'rarity_rank': rarity_rank[product],
            'product_quantity': len(rarity_rank),
            'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
            'product_favorite_list': product_favorite_list,
            'product_owner_list': product_owner_list,
        }
        return context

    def get(self, request, pk):
        context = self.get_context_data(pk)
        template_name = self.template_name
        return render(request, template_name, context)

    def post(self, request, pk):
        context = self.get_context_data(pk)
        product = context['product']

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
        
        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id', None)
            comment_type = request.POST.get('comment_type', None)
            comment_delete = None

            if comment_type == 'product':
                comment_delete = get_object_or_404(ProductComment, id=comment_id)
                comment_delete.delete()

            return JsonResponse({
                'comment_type': comment_type,
                'comment_delete': serializers.serialize('json', [comment_delete, ])
            })
        
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

        elif action == 'purchase_product':
            state = ''
            if request.user.property >= product.price and product.quantity > 0:
                # request.total_price -= product.price
                # if request.user.user_cart.products.filter(name=product.name).exists():
                #     request.user.user_cart.products.remove(product)

                # request.user.owners.add(product)
                # request.user.property -= product.price
                # request.user.save()
                # product.quantity -= 1
                # product.save()

                # TradeHistory.objects.create(
                #     buyer=request.user,
                #     seller=product.author,
                #     product=product,
                #     price_at_purchase=product.price,
                #     quantity_at_purchase=product.quantity
                # )
                
                state = 'can_buy'
            else:
                state = 'cant_buy'
            
            return JsonResponse({
                'state': state,
                'total_price': request.total_price,
                'user': serializers.serialize('json', [request.user, ]),
                'number_cart_products': len(request.user.user_cart.cart_products.all()),
                'product': serializers.serialize('json', [product, ])
            })

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class ArtworksView(View):
    template_name = 'NFTapp/explore/artworks/artworks{}.html'

    def get_context_data(self, classify_feature, classify_data):
        sort_data = classify_data
        sort_type = ' '.join([x.title() for x in sort_data.split('-')])

        users = User.objects.filter(is_superuser=0)
        products = NFTProduct.objects.filter(type_product__name='artworks')
        authors = [user for user in users if user.author.all().count()]

        context = {
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'users': users,
            'authors': authors,
            'sort_type': sort_type,
            'random_product': random.choice(products),
            'products': classify_feature(classify_data, products),
            # 'products': [product_list.pop(random.randint(0, len(product_list) - 1)) for i in range(len(product_list))],
        }
        return context

    def get(self, request, num, classify_feature):
        context = self.get_context_data(classify_feature, request.GET.get('sort-by', 'trending'))
        template_name = self.template_name.format(num)
        return render(request, template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class AboutUsView(View):
    template_name = 'NFTapp/community/about_us/about_us{}.html'

    def get_context_data(self):
        context = {
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
        }
        return context

    def get(self, request, num):
        context = self.get_context_data()
        template_name = self.template_name.format(num)

        if num == '1':
            products = NFTProduct.objects.all()
            users = User.objects.filter(is_superuser=0)
            comments = []
            topic = 'Alternate Medium Space'
            for product in products.filter(topic__name=topic):
                for comment in product.product_comments.all():      
                    comments.append(comment)
            context.update({
                'products': products,
                'users': users,
                'comments': comments,
                'topic': topic,
            })

        elif num == '2' or num == '3' or num == '5':
            titles = FAQTitle.objects.all()
            users = User.objects.filter(is_superuser=0)
            context.update({
                'titles': titles,
                'users': users,
            })

        elif num == '4':
            comments = []
            topic = 'Alternate Medium Space'
            for product in NFTProduct.objects.filter(topic__name=topic):
                for comment in product.product_comments.all():      
                    comments.append(comment)
            context.update({
                'comments': comments,
                'topic': topic,
            })
        return render(request, template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class ArtistsView(View):
    template_name = 'NFTapp/community/artists.html'

    def get_context_data(self):
        users = User.objects.filter(is_superuser=0).annotate(num_followers=Count('followers')).order_by('-num_followers')
        sort_data = self.request.GET.get('sort-by', 'follower')
        sort_type = ' '.join([x.title() for x in sort_data.split('-')])

        context = {
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'users': artists_classify(sort_data, users),
            'sort_type': sort_type
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class EditorialView(View):
    template_name = 'NFTapp/community/editorial.html'

    def get_context_data(self):
        users = User.objects.filter(is_superuser=0)
        products = NFTProduct.objects.all()

        context = {
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'users': users,
            'products': products
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class FAQsView(View):
    template_name = 'NFTapp/community/FAQs/FAQs{}.html'

    def get_context_data(self):
        titles = FAQTitle.objects.all()
        context = {
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'titles': titles
        }
        return context

    def get(self, request, num):
        context = self.get_context_data()
        template_name = self.template_name.format(num)
        return render(request, template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class BlogView(View):
    template_name = 'NFTapp/blog/blog.html'

    def get_context_data(self):
        blogs = NFTBlog.objects.all().order_by('image')
        products = NFTProduct.objects.all()
        users = User.objects.filter(is_superuser=0)
        comments = []
        topic = 'Alternate Medium Space'
        for product in products.filter(topic__name=topic):
            for comment in product.product_comments.all():
                comments.append(comment)
        
        context = {
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'blogs': blogs,
            'products': products,
            'users': users,
            'comments': comments,
            'topic': topic
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

@method_decorator(add_search_data, name='dispatch')
@method_decorator(add_cart_data, name='dispatch')
class BlogDetailView(View):
    template_name = 'NFTapp/blog/blog_detail.html'

    def get_context_data(self, pk):
        blogs = NFTBlog.objects.all()
        blog_detail = get_object_or_404(NFTBlog, pk=pk)
        random_blogs = list(blogs).copy()
        random_blogs.remove(blog_detail)
        blogs_more = [random_blogs.pop(random.randint(0, len(random_blogs) - 1)) for i in range(3)]

        comments = blog_detail.blog_comments.all()
        
        context = {
            'type_comment': 'blog',
            'cart_products': self.request.cart_products,
            'search_data': self.request.search_data,
            'blog_detail': blog_detail,
            'blogs': blogs_more,
            'comments': comments,
        }
        return context

    def get(self, request, pk):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def post(self, request, pk):
        context = self.get_context_data(pk)
        action = request.POST.get('action', None)
        blog_detail = context['blog_detail']
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
        
        elif action == 'delete_comment':
            comment_id = request.POST.get('comment_id', None)
            comment_type = request.POST.get('comment_type', None)
            comment_delete = None

            if comment_type == 'blog':
                comment_delete = get_object_or_404(BlogComment, id=comment_id)
                comment_delete.delete()

            return JsonResponse({
                'comment_type': comment_type,
                'comment_delete': serializers.serialize('json', [comment_delete, ])
            })
        
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
