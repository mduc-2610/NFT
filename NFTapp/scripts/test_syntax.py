# def run():
#     d = {
#         'a': {
#             'b': 1
#         }
#     }
#     print(d.a.b)

from math import ceil
import random
import os
from datetime import datetime
from faker import Faker
from PIL import Image
from django.core.management.base import BaseCommand
from NFTapp.models import User, NFTProduct, Topic, OwnerNFTProduct, Type, NFTBlog, Comment, BlogSection
from NFT.settings import MEDIA_ROOT
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
    print(NFTProduct.objects.all().get(image="/static/images/explore/collection/nft_image12.svg").id)