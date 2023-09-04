from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        print("POST request received")  # Debug print

        # Process the POST request
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')

        # Debug print
        print(first_name, last_name, email)

        # Update your custom fields here
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        
        # Don't forget to save the user object to commit changes
        try:
            user.save()
            messages.success(request, 'Your profile has been updated!')
        except Exception as e:
            print(f"An error occurred while saving the user: {e}")
            messages.error(request, 'An error occurred while updating your profile.')

        # Redirect to the same profile page to display the updated info
        return redirect('MiBarrioApp:profile')

    # If a GET request, display the profile page as usual
    context = {'user': user}
    return render(request, 'profile.html', context)

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
