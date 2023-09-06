from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SearchProfiles
from django.http import JsonResponse
import json

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
    form_type = request.POST.get('form_type')

    if request.method == 'POST':
        if form_type == 'profile':

            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')

            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email

            try:
                user.save()
                messages.success(request, 'Your profile has been updated!')
            except Exception as e:
                print(f"An error occurred while saving the user: {e}")
                messages.error(request, 'An error occurred while updating your profile.')
            return redirect('MiBarrioApp:profile')

        elif form_type == 'search_profile':
            print("Processing search_profile form")

            sp_name = request.POST.get('sp_name')
            age = request.POST.get('age')

            social_cultural = request.POST.getlist('social_cultural[]')
            health_wellness = request.POST.getlist('health_wellness[]')
            leisure_recreation = request.POST.getlist('leisure_recreation[]')
            community_services = request.POST.getlist('community_services[]')

            social_cultural_levels = request.POST.get('socialLikert')
            health_wellness_levels = request.POST.get('healthLikert')
            leisure_recreation_levels = request.POST.get('leisureLikert')
            community_services_levels = request.POST.get('communityLikert')

            # Mandatory field checks
            mandatory_fields = [
                sp_name, age, social_cultural, health_wellness, leisure_recreation, community_services,
                social_cultural_levels, health_wellness_levels, leisure_recreation_levels, community_services_levels
            ]

            if not all(mandatory_fields):
                messages.error(request, 'Not all mandatory fields are completed.')
                return redirect('MiBarrioApp:profile')

            transportation_active = request.POST.get('transportation_active') == 'on'
            transportation_public = request.POST.get('transportation_public') == 'on'
            backup_power_supply = request.POST.get('backup_power_supply') == 'on'
            backup_water_supply = request.POST.get('backup_water_supply') == 'on'

            try:
                print("Trying to save search profile...")  # Add this
                search_profile = SearchProfiles.objects.create(
                    user=user,
                    sp_name=sp_name,
                    age=age,
                    # Serialize the list to string
                    social_cultural_tags=json.dumps(social_cultural),
                    health_wellness_tags=json.dumps(health_wellness),
                    leisure_recreation_tags=json.dumps(leisure_recreation),
                    community_services_tags=json.dumps(community_services),
                    social_cultural_levels=social_cultural_levels,
                    health_wellness_levels=health_wellness_levels,
                    leisure_recreation_levels=leisure_recreation_levels,
                    community_services_levels=community_services_levels,
                    transportation_active=transportation_active,
                    transportation_public=transportation_public,
                    backup_power_supply=backup_power_supply,
                    backup_water_supply=backup_water_supply
                )
                search_profile.save()
                messages.success(request, 'Your search profile has been saved!')
            except Exception as e:
                print(f"An error occurred while saving the search profile: {e}")
                messages.error(request, 'An error occurred while saving your search profile.')

            return redirect('MiBarrioApp:profile')

    # If a GET request, display the profile page as usual
    user_search_profiles = SearchProfiles.objects.filter(user=request.user)
    context = {'user': user, 'search_profiles': user_search_profiles}
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
