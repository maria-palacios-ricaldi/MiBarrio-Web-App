from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SearchProfiles, Searches, SearchResults, Suburbs, Cities, CustomUser, SuburbStatistics
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from sklearn.neighbors import NearestNeighbors
import logging
import pandas as pd
import numpy as np
import os
from django.utils import timezone
import pprint

# Create your views here.

logger = logging.getLogger(__name__)

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
            editingSpId = request.POST.get('editingSpId')

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

            # Function to update or create a search profile
            def save_search_profile(sp=None):
                sp.sp_name = sp_name
                sp.age = age
                sp.social_cultural_tags = json.dumps(social_cultural)
                sp.health_wellness_tags = json.dumps(health_wellness)
                sp.leisure_recreation_tags = json.dumps(leisure_recreation)
                sp.community_services_tags = json.dumps(community_services)
                sp.social_cultural_levels = social_cultural_levels
                sp.health_wellness_levels = health_wellness_levels
                sp.leisure_recreation_levels = leisure_recreation_levels
                sp.community_services_levels = community_services_levels
                sp.transportation_active = transportation_active
                sp.transportation_public = transportation_public
                sp.backup_power_supply = backup_power_supply
                sp.backup_water_supply = backup_water_supply
                sp.save()


            if editingSpId:
                try:
                    search_profile = SearchProfiles.objects.get(search_profileID=editingSpId)
                    save_search_profile(search_profile)
                    messages.success(request, 'Your search profile has been updated!')
                except SearchProfiles.DoesNotExist:
                    messages.error(request, 'Search profile not found.')

            else:
                #Creating a new search profile
                try:
                    print("Trying to save search profile...")  # Add this
                    search_profile = SearchProfiles.objects.create(
                    user=user,
                    sp_name=sp_name,
                    #age=age,
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
                    save_search_profile(search_profile)
                    messages.success(request, 'Your search profile has been saved!')

                except Exception as e:
                    # Log the exception
                    print(f"An error occurred while saving the search profile: {e}")
                    messages.error(request, 'An error occurred while saving your search profile.')

            return redirect('MiBarrioApp:profile')

    # If a GET request, display the profile page as usual
    user_search_profiles = SearchProfiles.objects.filter(user=request.user)
    context = {'user': user, 'search_profiles': user_search_profiles}
    return render(request, 'profile.html', context)


def new_search_view(request):
    context = {}  # Initialize context dictionary

    if request.user.is_authenticated:
        print("User is authenticated")
        search_profiles = SearchProfiles.objects.filter(user=request.user)
        context['search_profiles'] = search_profiles  # Set search_profiles

        action_type = request.POST.get('action_type', None)

        if request.method == 'POST':
            print("POST received")

            selected_profile_id = request.POST.get('selected_profile', None)
            print(f"Received selected_profile_id from POST request: {selected_profile_id}")
            request.session['selected_profile_id'] = selected_profile_id
            context['selected_profile_id'] = selected_profile_id  # Set selected_profile_id

            if action_type == 'search' and selected_profile_id:

                selected_profile = SearchProfiles.objects.filter(user=request.user, search_profileID=selected_profile_id).first()
                #nearest neighbors logic

                print("Inside action_type == 'search' block")  # Debugging Line

                if selected_profile:

                # Create a category mapping based on tags
                    category_mapping = {
                        'Social & Cultural Activities': json.loads(selected_profile.social_cultural_tags),
                        'Health & Wellness': json.loads(selected_profile.health_wellness_tags),
                        'Leisure & Recreation': json.loads(selected_profile.leisure_recreation_tags),
                        'Community & Services': json.loads(selected_profile.community_services_tags),
                    }
                    print("Category mapping based on tags:", category_mapping)

                    user_input = {
                        'Social & Cultural Activities': selected_profile.social_cultural_levels,
                        'Health & Wellness': selected_profile.health_wellness_levels,
                        'Leisure & Recreation': selected_profile.leisure_recreation_levels,
                        'Community & Services': selected_profile.community_services_levels,
                        'Public Transportation': selected_profile.transportation_public,
                        'Active Transportation': selected_profile.transportation_active
                    }
                    print("User input for this search:", user_input)

                    # Saving the search in the Searches model
                    search_parameters = {
                        'city': request.POST.get('citySelect'),
                        'user_input': user_input,
                        'category_mapping': category_mapping,
                    }
                    search_parameters_str = json.dumps(search_parameters)

                    new_search = Searches(
                    user=request.user,
                    search_profileID=SearchProfiles.objects.get(search_profileID=selected_profile_id),
                    search_parameters=search_parameters_str,
                    search_timestamp=datetime.now()
                    )
                    #saves new Search to Searches model
                    new_search.save()

                    df = read_my_csv()

                    averaged_df = pd.DataFrame()
                    averaged_df['Suburb_name'] = df['Suburb_name']
                    averaged_df['Coordinates'] = df['Coordinates']

                    for category, amenities in category_mapping.items():
                        user_score = user_input.get(category, 1)
                        if user_score > 1:
                            averaged_df[category] = df[amenities].mean(axis=1).apply(lambda x: round(x))

                    if user_input.get('Public Transportation', False):
                        averaged_df['Public Transportation'] = df['Public Transportation']
                    elif user_input.get('Active Transportation', False):
                        averaged_df['Active Transportation'] = df['Active Transportation']

                    available_categories = [category for category in category_mapping.keys() if category in averaged_df.columns]

                    ordered_categories = sorted(
                        available_categories,
                        key=lambda category: abs(user_input.get(category, 0) - averaged_df[category].mean()),
                        reverse=True
                    )

                    selected_features = averaged_df[ordered_categories]
                    if selected_features is None:
                        print("Selected features is None.")


                    nn_model = NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
                    nn_model.fit(selected_features)


                    print(f"Selected features for profile {selected_profile_id}: {selected_features}")

                    user_preferences = [user_input[category] for category in ordered_categories]
                    distances, indices = nn_model.kneighbors([user_preferences])


                    nearest_suburbs = averaged_df.iloc[indices[0]][['Suburb_name', 'Coordinates']]
                    print("Top 5 best suburbs for the user:")

                    print(nearest_suburbs.head())

                    if nearest_suburbs is not None:
                        for _, row in nearest_suburbs.iterrows():
                            suburb_name = row['Suburb_name']

                            # Fetch the Suburbs object based on the suburb_name
                            suburb_record = Suburbs.objects.filter(name=suburb_name).first()
                            if suburb_record:
                                # Create a SearchResults record associating the suburb with the new search
                                SearchResults.objects.create(search=new_search, suburb=suburb_record)

                    print(f'Added a new searchResults to the database')
                    # Get the names and coordinates of the suburbs related to the current search
                    current_search_suburbs = SearchResults.objects.filter(search=new_search).values('suburb__name', 'suburb__coordinates')

                    # Transform the QuerySet into a list of dictionaries for easier use in JavaScript
                    current_search_suburbs_list = list(current_search_suburbs)

                    # Add to your context dictionary
                    context['nearest_suburbs'] = json.dumps(current_search_suburbs_list)



        else:
            selected_profile_id = request.session.get('selected_profile_id', None)

        if selected_profile_id:
            selected_profile = SearchProfiles.objects.filter(user=request.user, search_profileID=selected_profile_id).first()
        else:
            selected_profile = search_profiles.first()

        if selected_profile:
            selected_profile_data = {
                'search_profileID': selected_profile.search_profileID,
                'social_cultural_tags': json.loads(selected_profile.social_cultural_tags),
                'health_wellness_tags': json.loads(selected_profile.health_wellness_tags),
                'leisure_recreation_tags': json.loads(selected_profile.leisure_recreation_tags),
                'community_services_tags': json.loads(selected_profile.community_services_tags),
                'social_cultural_levels': selected_profile.social_cultural_levels,
                'health_wellness_levels': selected_profile.health_wellness_levels,
                'leisure_recreation_levels': selected_profile.leisure_recreation_levels,
                'community_services_levels': selected_profile.community_services_levels,
                'transportation_active': selected_profile.transportation_active,
                'transportation_public': selected_profile.transportation_public,
                'backup_power_supply': selected_profile.backup_power_supply,
                'backup_water_supply': selected_profile.backup_water_supply,
            }
            context['selected_profile_data'] = json.dumps(selected_profile_data, cls=DjangoJSONEncoder, ensure_ascii=True).replace('"', '&quot;')
            context['test_data'] = 'some_test_data1'  # Set test_data

        else:
            context['test_data'] = 'some_test_data2'  # Set test_data

        print('About to render template.')
        print(f'context: {context}')
        return render(request, 'newSearch.html', context)

    else:
        return redirect('login')


# views.py
def test_view(request):
    context = {'test_data': 'some_test_data'}
    return render(request, 'test_template.html', context)


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

# --------------------------- HELPER FUNCTIONS -------------------------->

# Helper function to read the CSV file
def read_my_csv():
    project_dir = os.path.dirname(os.path.abspath(__file__))  # get the current directory
    csv_file_path = os.path.join(project_dir, 'data', 'filtered_suburbs_amenity_scores.csv')
    df = pd.read_csv(csv_file_path)
    return df  # can perform any data manipulations needed before returning

@csrf_exempt
def get_nearest_suburbs(request):
    if request.method == "POST":
        selected_profile_id = request.POST.get('selected_profile_id', None)

        if selected_profile_id is not None:
            # Get the latest search for this profile
            latest_search = Searches.objects.filter(search_profileID=selected_profile_id).latest('search_timestamp')

            if latest_search:
                # Get the nearest suburbs associated with this search
                nearest_suburbs_qs = SearchResults.objects.filter(search=latest_search).values('suburb__name', 'suburb__coordinates')

                # Convert to list of dictionaries
                nearest_suburbs_list = list(nearest_suburbs_qs)

                print(f"Nearest Suburbs List: {json.dumps(nearest_suburbs_list, indent=4)}")  # Debugging line

                return JsonResponse({'nearest_suburbs': nearest_suburbs_list})
            else:
                return JsonResponse({'error': 'No search results found'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid profile ID'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_crime_data(request, suburb_name):
    try:
        suburb_stats = SuburbStatistics.objects.get(suburb__name=suburb_name)
        return JsonResponse({'crime_rate': suburb_stats.crime_rate})
    except SuburbStatistics.DoesNotExist:
        return JsonResponse({'error': 'Suburb not found'}, status=404)
