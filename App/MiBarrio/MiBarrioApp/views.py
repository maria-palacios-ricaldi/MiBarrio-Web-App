from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm

# Create your views here.

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

def about_us_view(request):
    return render(request, 'aboutUs.html', {})

def profile_view(request):
    return render(request, 'profile.html', {})

def new_search_view(request):
    return render(request, 'newSearch.html', {})

def new_search_2_view(request):
    return render(request, 'newSearch2.html', {})

def new_search_3_view(request):
    return render(request, 'newSearch3.html', {})

def view_past_searches_view(request):
    return render(request, 'viewPastSearches.html', {})

def feedback_view(request):
    return render(request, 'feedback.html', {})

def contact_us_view(request):
    return render(request, 'contactUs.html', {})
