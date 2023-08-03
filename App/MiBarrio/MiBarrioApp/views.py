from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm

# Create your views here.
#def index_page(request) :
    #return HttpResponse("First App")
    #return render(request, "index.html", {})

def home_view(request):
    return render(request, 'home.html', {})

def login_view(request):
    return render(request, 'login.html', {})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
