from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    context = {
        'hello': 'hellosss'
    }
    return render(request, 'main.html', context)
