from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#def index_page(request) :
    #return HttpResponse("First App")
    #return render(request, "index.html", {})

def home_view(request):
    return render(request, 'home.html', {})

def login_view(request):
    return render(request, 'login.html', {})
