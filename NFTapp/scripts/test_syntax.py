# def run():
#     d = {
#         'a': {
#             'b': 1
#         }
#     }
#     print(d.a.b)

from collections import Counter
from math import ceil
import random
import os
from datetime import datetime
from faker import Faker
from PIL import Image
from django.core.management.base import BaseCommand
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite, \
                                VoteProductComment, VoteBlogComment, \
                                DisvoteProductComment, DisvoteBlogComment, \
                                Follow, Cart, CartItem
from NFT.settings import MEDIA_ROOT

from django.db.models import Count, Q
fake = Faker()

def run():
#     blogs_context = {}
#     blogs = NFTBlog.objects.all().order_by('image')
#     average_wpm = 238
#     for blog in blogs:
#         words_of_blog = sum([len(str(section.content).split()) for section in blog.blog_section.all()])
#         blogs_context[blog] = ceil(words_of_blog / average_wpm)

#     blog_detail = NFTBlog.objects.get(pk='0b1d8c2ab5b842e5a0d8e70aef14d594')
#     context = {
#         'blog': [blog_detail, blogs_context[blog_detail]]
#     }
#     print(context['blog'])


    # users = User.objects.all()
    # authors = []
    # for user in users:
    #     res = user.author.all().count()
    #     print(user, res)
    #     if res:
    #         authors.append(user)

    # print(authors)

    # print(round(random.uniform(0, 3), 8))
    # print("Product", NFTProduct.objects.all().get(image="/static/images/explore/collection/nft_image11.svg").id)
    # print("User", User.objects.all()[5].id)
    # user = User.objects.all()[1]
    # # product = NFTProduct.objects.get(image="/static/images/explore/collection/nft_image11.svg")
    # print(user.name)
    # [print(f"{product.id} {product.name} {product.topic.name}") for product in  user.nftproduct_set.all()]

    # print(len(user.nftproduct_set.all()))
#     user = User.objects.get(pk="37083387-c510-4088-984b-f1ea7c7379a9")
#     context = {
#         "user": user,
#         # "url_method": request.GET.get('filter', 'collection')
#     }
#     # if request.GET.get('href') == "?collection":
#     product_collection = user.nftproduct_set.all()
#     context["products"] = product_collection
# # elif request.GET.get('href') == "?created":
#     product_created = user.author.all()
#     context["products1"] = product_created  
# # else:
#     product_favorited = user.likes.all()
#     context["products2"] = product_favorited
#     {print(k, v) for k, v in context.items()}

    # type_instance = Type.objects.get(name="artworks")
    # products = NFTProduct.objects.filter(type_product__name="artworks")
    # # print(type_instance)
    # products = type_instance.products_type.all()
    # print(len(products))
    # [print(product) for product in products]

    # print(FAQTitle.objects.filter(title="Enjin"))
    # print(NFTProduct.objects.annotate(num_owners=Count('owners')).order_by('-num_owners'))
    # products = NFTProduct.objects.all()
    # comments = []
    # for product in products.filter(topic__name="ALternate Medium Space"):
    #     for comment in product.product_comments.all():      
    #         comments.append(comment) 
    # # print(comments[0].user_product_comments.all())
    # for comment in comments:
    # #     print(f"{comment.user.id} {comment.content}")

    # product = NFTProduct.objects.get(image="/static/images/explore/collection/nft_image1.svg")
    # product_favorite_list = product.favorites.all()
    # product_favorite_list_2 = product.favorites_by.all()
    # for product in product_favorite_list:
    #     print(product)
    # for product in product_favorite_list_2:
    #     print(product)

    # user = User.objects.get(name="smithbrandy")
    
    # [print(user) for user in user.owners.all()]
    # print("___________________________________________")
    # product = NFTProduct.objects.get(name="PixelPrestige")
    # # print(product)
    # print(type(Topic.objects.values()))
    # [print(pro) for pro in Topic.objects.values()]

    # [print(product) for product in user.owned_products.all()]
    # print("_________________________________________________")
    # [print(product) for product in user.nftproduct_set.all()]
    # [print(favorite.user, favorite.product, sep="\t\t") for favorite in product_favorite_list]
    # print("________________________________________________________________")
    # product_owner_list = product.owners.all()
    # [print(owner) for owner in product_owner_list]

    # print(User.objects.all()[2])

    # user_search = []
    # for user in User.objects.filter(is_superuser=0).values():
    #     user_search.append(user['id'])
    
    # product_search = []
    # for product in NFTProduct.objects.values():
    #     product_search.append(product['id'])

    # blog_search = []
    # for blog in NFTBlog.objects.values():
    #     blog_search.append(blog['id'])

    # search_data = user_search + product_search + blog_search
    
    # print(search_data)
    # x = None
    # x.y = 1
    # print(x)

    # def s(a, b):
    #     print(a, b)
    # s(b=1, a=100)
    # d = {
    #     'a': 'aaa',
    #     'b': 'bbb',
    # }

    # print(d.pop('a'))
    # print(d)

    # print([1] + [2] + [3])
    # users = User.objects.filter(is_superuser=0).annotate(num_products=Count('owners')).order_by('-num_products')
    # print(users)
    # user = User.objects.all()[5]
    # [print(user) for user in user["follower_set"].all()]
    # print("________________________________________________________________")
    # [print(user) for user in user["following_set"].all()]
    # product = NFTProduct.objects.all()[6]
    # [[print(vote) for vote in product.votes.all()] for product in product.product_comments.all()]
    # [print(vote.comment) for vote in product.product_comments.all()[2].product_comment_voted_by.all()]
    # cart = Cart.objects.get(user=user).cart_products.all()
    
    # [print(product) for product in Cart.objects.get(user=User.objects.get(id="17514970-75fa-4586-9781-7de6460c15b2")).products.all()]
    # print(len([print(product) for product in Cart.objects.get(user=User.objects.get(id="17514970-75fa-4586-9781-7de6460c15b2")).products.all()]))
    # product_favorite_list = product.favorites_by.all()
    # [print(product) for product in product_favorite_list]

    # user__ = User.objects.get(id="233c3b24-01b5-4716-bb95-5866bf516831")
    # # print(user__.id, end="\n\n\n")
    # [print(user.follower.id) for user in user__.follower_set.all()]

    # product_comment = ProductComment.objects.get(id="3245")
    # [print(user) for user in product_comment.votes.all()]
    # print(VoteProductComment.objects.get(user=User.objects.get(id="1380fd40-aac0-4a10-94ff-54dac9e0b623"), comment=ProductComment.objects.get(id='3242')))
    

    # user = User.objects.all()[5]
    # print(user.user_cart)
    # [print(product) for product in NFTProduct.objects.all()]
    # [print(product) for product in user.user_cart.cart_products.all()]
    # print("_____________________________________")
    # [print(product) for product in user.owners.all()]
    # print("YES") if NFTProduct.objects.get(id="0a958ed4-2042-4ecc-83a2-08bf623ff7d8") not in [item.product for item in user.user_cart.cart_products.all()] else print("NO")
    # print(NFTProduct.objects.get(id="0a958ed4-2042-4ecc-83a2-08bf623ff7d8").id)
    # print(Cart.objects.get(user=user).products.all())
    # [print(product.price) for product in Cart.objects.get(user=user).products.all()]
    # product = NFTProduct.objects.all()[1]
    # print(product)
    # [print(product) for product in user.owners.all()]
    # [print(product.product) for product in user.user_cart.cart_products.all()]
    # blog = NFTBlog.objects.all()[1]
    # # [print(comment) for comment  in blog.blog_comments.all()]
    # for comment in blog.blog_comments.all():
    #     print(comment)
    #     for vote in comment.blog_comment_disvoted_by.all():
    #         print(f"\t{vote.user}, {vote.comment}")

    # a = {
    #     'name' :' Duc',
    # }

    # a = {
    #     'age': 19
    # }
    # print(a)
    # user = User.objects.all()[6]
    # [print(product) for product in user.user_cart.products.all()]

    # product = NFTProduct.objects.all()[5]
    # print(product.sold())
    # # print(product.annotate(num_created=Count('author')).order_by('-num_created'))
    

    # print(user.sold())
    # import pytz
    # vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')    
    # now = datetime.now(vietnam_timezone)
    # value = NFTProduct.objects.all()[5].created_at
    # print(now.time(), value.time())
    # time_difference = now.microsecond / 1000 - value.microsecond / 1000
    # print(now.microsecond, value.microsecond)

    # user = User.objects.all()[5]
    # trades = user.buyer_trades.all()
    # [print(trade.product) for trade in trades]
    # def hello(name):
    #     return 'Hello' + name
    # a =  {
    #     'hello': hello
    # }
    # print(a['hello']('DUC'))


    user = User.objects.all()[5]
    print(user, user.total_earned())
    for product in user.author.all():
        print(product.price, len(product.owners.all()))

    for owner in product.owners.all():
        print(owner)