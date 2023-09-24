from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='%Y/%m/%d/')
    bio = models.CharField(max_length=300)
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'password']

class NFTProduct(models.Model):
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    owners = models.ManyToManyField(User, through="OwnerNFTProduct", related_name="owned_nft_products")
    authors = models.ManyToManyField(User, through="AuthorNFTProduct")
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    quantity = models.PositiveIntegerField()
    descriptiton = models.TextField(null=True)
    

    def __str__(self):
        return f"{self.name} {self.price}"

class Topic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class OwnerNFTProduct(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(NFTProduct, on_delete=models.CASCADE)

class AuthorNFTProduct(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(NFTProduct, on_delete=models.CASCADE)
