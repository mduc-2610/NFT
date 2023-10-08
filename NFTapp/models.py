import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', default="/static/images/generic/default_avatar.svg")
    bio = models.CharField(max_length=300)
    # creator = models.BooleanField(default=False)
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'password']
    
    def __str__(self):
        return f"{self.name} {self.email}"

class NFTProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    owners = models.ManyToManyField(User, through="OwnerNFTProduct")
    author = models.ForeignKey('User', related_name= "author", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f"nft_product_images/%Y/%m/%d/")
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=True)
    stars = models.SmallIntegerField(default=1)
    type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True)
    artwork = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return f"{self.name} {self.price}"

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

class Comment(models.Model):
    product = models.ForeignKey(NFTProduct, related_name="product_comments", on_delete=models.CASCADE)
    blog = models.ForeignKey('NFTBlog', related_name="blog_comments", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User,related_name="user_comments", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.product.name} {self.user.name}"
    
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
    title = models.ForeignKey(FAQTitle, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question