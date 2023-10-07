from django.contrib import admin
from NFTapp.models import User, NFTProduct, Topic, OwnerNFTProduct, Type, NFTBlog, Comment, BlogSection
# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(NFTProduct)
admin.site.register(OwnerNFTProduct)
admin.site.register(Type)
admin.site.register(NFTBlog)
admin.site.register(Comment)
admin.site.register(BlogSection)