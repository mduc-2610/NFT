from django.contrib import admin
from NFTapp.models import User, NFTProduct, Topic,\
                             OwnerNFTProduct, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle 

models_to_register = [User, Topic, NFTProduct, OwnerNFTProduct, Type,
                      NFTBlog, BlogSection, FAQ, FAQTitle]

for model in models_to_register:
    admin.site.register(model)