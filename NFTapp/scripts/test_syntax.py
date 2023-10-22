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
                                FAQ, FAQTitle
from NFT.settings import MEDIA_ROOT

from django.db.models import Count
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

    user = User.objects.get(name="lisa45")
    [print(f"{user.name}: {user.password}\n") for user in User.objects.all()]
    # [print(product) for product in user.owned_products.all()]
    # print("_________________________________________________")
    # [print(product) for product in user.nftproduct_set.all()]
    # [print(favorite.user, favorite.product, sep="\t\t") for favorite in product_favorite_list]
    # print("________________________________________________________________")
    # product_owner_list = product.owners.all()
    # [print(owner) for owner in product_owner_list]

    # print(User.objects.all()[2])