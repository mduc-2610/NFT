import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random

# Create your models here.
default_cover_photos = ['/static/images/generic/Acer_Wallpaper_01_3840x2400.jpg',
                  '/static/images/generic/Acer_Wallpaper_02_3840x2400.jpg',
                  '/static/images/generic/Acer_Wallpaper_03_3840x2400.jpg',
                  '/static/images/generic/Acer_Wallpaper_04_3840x2400.jpg',
                  '/static/images/generic/Acer_Wallpaper_05_3840x2400.jpg']
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', default="/static/images/generic/default_avatar.svg")
    cover_photo = models.ImageField(upload_to='avatar/%Y/%m/%d/', default=random.choice(default_cover_photos)) 
    bio = models.CharField(max_length=300)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    # creator = models.BooleanField(default=False)
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'password']
    
    def __str__(self):
        return f"{self.name} {self.email}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')

class NFTProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=4)
    rarity = models.DecimalField(max_digits=6, decimal_places=4)
    owners = models.ManyToManyField(User, through="OwnerNFTProduct")
    author = models.ForeignKey('User', related_name= "author", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f"nft_product_images/%Y/%m/%d/")
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=True)
    favorites = models.ManyToManyField(User, related_name="favorites", through='NFTProductFavorite', default=0)
    type_product = models.ForeignKey('Type', related_name="products_type",on_delete=models.SET_NULL, null=True)
    artwork = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return f"{self.name} {self.price}"


class NFTProductFavorite(models.Model):
    product = models.ForeignKey('NFTProduct', related_name='favorites_by', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='favorite_products', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} {self.user.name}"

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(NFTProduct, related_name="products", through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.product.price for item in self.cart_items.all())

    def __str__(self):
        return f"Cart for {self.owner}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(NFTProduct, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in Cart"

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
class OwnerNFTProduct(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(NFTProduct, on_delete=models.CASCADE)
    # author = models.BooleanField()
    
class NFTBlog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name="blog_author", on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=f"blog/title/%Y/%m/%d/", null=True)

    def __str__(self):
        return f"{self.title}"
    
class BlogSection(models.Model):
    image = models.ImageField(upload_to=f"blog/section/%Y/%m/%d/", null=True)
    blog = models.ForeignKey(NFTBlog, related_name="blog_section", on_delete=models.CASCADE, null=True)
    heading = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.heading}"
    

class FAQTitle(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class FAQ(models.Model):
    title = models.ForeignKey(FAQTitle, related_name="questions", on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
# class Comment(models.Model):
#     product = models.ForeignKey(NFTProduct, related_name="product_comments", on_delete=models.CASCADE, default=-1)
#     blog = models.ForeignKey('NFTBlog', related_name="blog_comments", on_delete=models.CASCADE, default=-1)
#     user = models.ForeignKey(User,related_name="user_comments", on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     content = models.TextField()

#     def __str__(self):
#         return f"{self.product.name} {self.user.name}"
    
class Comment(models.Model):
    vote = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        abstract = True 

    def __str__(self):
        return f"{self.user.username}"

class ProductComment(Comment):
    user = models.ForeignKey(User, related_name="user_product_comments", on_delete=models.CASCADE)
    product = models.ForeignKey('NFTProduct', related_name="product_comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} {self.user.name}"

class BlogComment(Comment):
    user = models.ForeignKey(User, related_name="user_blog_comments", on_delete=models.CASCADE)
    blog = models.ForeignKey('NFTBlog', related_name="blog_comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blog.title} {self.user.name}"