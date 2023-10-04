from django.shortcuts import render, HttpResponse
from NFTapp.models import User, NFTProduct, Topic, OwnerNFTProduct, Type

# Create your views here.
def home(request):
    context = {
        'hello': 'hellosss'
    }
    return render(request, 'NFTapp/home/home1.html', context)

def home2(request):
    context = {
        'hello': 'hellosss'
    }
    return render(request, 'NFTapp/home/home2.html', context)

def home5(request):
    context = {
        'hello': 'hellosss'
    }
    return render(request, 'NFTapp/home/home5.html', context)

def collection1(request):
    products = NFTProduct.objects.all()
    context = {
        "products": products
    }
    return render(request, 'NFTapp/explore/collection/collection1.html', context)