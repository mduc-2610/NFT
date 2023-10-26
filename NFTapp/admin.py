from django.contrib import admin
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite, \
                                VoteProductComment, VoteBlogComment

models_to_register = [User, Topic, NFTProduct, NFTProductOwner, Type,
                      NFTBlog, BlogSection, FAQ, FAQTitle, NFTProductFavorite, VoteProductComment, VoteBlogComment]

for model in models_to_register:
    admin.site.register(model)