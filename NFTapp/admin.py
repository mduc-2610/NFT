from django.contrib import admin
from NFTapp.models import User, NFTProduct, Topic,\
                             NFTProductOwner, Type, NFTBlog, \
                                BlogSection, BlogComment, ProductComment,\
                                FAQ, FAQTitle, NFTProductFavorite, \
                                VoteProductComment, VoteBlogComment

models_to_register = [Topic, NFTProduct, NFTProductOwner, Type,
                      NFTBlog, BlogSection, FAQ, FAQTitle, NFTProductFavorite, VoteProductComment, VoteBlogComment]

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')

admin.site.register(User, UserAdmin)

for model in models_to_register:
    admin.site.register(model)
