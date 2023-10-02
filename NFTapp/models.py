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
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', default="generic/default_avatar.svg")
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    bio = models.CharField(max_length=300)
    creator = models.BooleanField(default=False)
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'password']
    
    def __str__(self):
        return f"{self.name} {self.email} {self.creator}"

class NFTProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    owners = models.ManyToManyField(User, through="OwnerNFTProduct")
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f"{name}/%Y/%m/%d/")
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

class Author(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"
