from django.shortcuts import render, HttpResponse

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