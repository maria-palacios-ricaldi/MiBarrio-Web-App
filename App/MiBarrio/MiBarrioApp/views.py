from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SearchProfiles, Searches, SearchResults, Suburbs, PropertiesToBuy, PropertiesToRent, SuburbStatistics, Feedback, Properties
from django.http import JsonResponse
from .forms import ContactForm
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json
from django.core.serializers.json import DjangoJSONEncoder
from sklearn.neighbors import NearestNeighbors
import logging
import pandas as pd
import numpy as np
import os
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

logger = logging.getLogger(__name__)

@login_required
def home_view(request):
    return render(request, 'home.html', {})

def login_view(request):
    return render(request, 'login.html', {})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MiBarrioApp:login')
        else:
            print(form.errors)  # Print validation errors to the console
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

@login_required
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

                    try:
                        new_search = Searches(
                            user=request.user,
                            search_profileID=SearchProfiles.objects.get(search_profileID=selected_profile_id),
                            search_parameters=search_parameters_str,
                            search_timestamp=datetime.now()
                     )

                        #saves new Search to Searches model
                        new_search.save()
                        print("new Search is saved")
                    except Exception as e:
                        print(f"Exception occurred: {e}")

                    df = read_my_csv()
                    print(df.columns)

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

                    nn_model = NearestNeighbors(n_neighbors=5, algorithm='ball_tree')
                    nn_model.fit(selected_features)

                    #print(f"Selected features for profile {selected_profile_id}: {selected_features}")

                    user_preferences = [user_input[category] for category in ordered_categories]
                    distances, indices = nn_model.kneighbors([user_preferences])

                    nearest_suburbs = averaged_df.iloc[indices[0]][['Suburb_name', 'Coordinates']]
                    print("Top 5 best suburbs for the user:")

                    if nearest_suburbs is not None:
                        for _, row in nearest_suburbs.iterrows():
                            suburb_name = row['Suburb_name']
                            print(suburb_name)

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

                    # Add to context dictionary
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

        return render(request, 'newSearch.html', context)

    else:
        return redirect('login')


# views.py
def test_view(request):
    context = {'test_data': 'some_test_data'}
    return render(request, 'test_template.html', context)

@login_required
@csrf_exempt
def new_search_2_view(request):
    message = ""
    result_dict = []

    if request.method == "POST":
        # Extract query parameters from the POST request
        suburb = request.POST.get("suburb")
        property_type = request.POST.get("property_type")
        rent_sale = request.POST.get("rent_sale")
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        back_up_power = request.POST.get("back_up_power") == "True"
        back_up_water = request.POST.get("back_up_water") == "True"

        # Debugging print statements
        print(f'Suburb: {suburb}')
        print(f'Property Type: {property_type}')
        print(f'Rent/Sale: {rent_sale}')
        print(f'Min Price: {min_price}')
        print(f'Max Price: {max_price}')
        print(f'Back Up Power: {back_up_power}')
        print(f'Back Up Water: {back_up_water}')

        # Get the path to the CSV file
        base_dir = os.path.dirname(os.path.abspath(__file__))  # This will get the directory of views.py
        data_dir = os.path.join(base_dir, 'data')

        if property_type == "Apartment or Flat":
            file_path = os.path.join(data_dir, 'Apartments_cpt.csv')
        else:
            file_path = os.path.join(data_dir, 'Apartments_cpt_updated.csv')

        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path, delimiter=';')

        df = df.rename(columns={
            'Suburb Name': 'Suburb_Name',
            'backup water': 'backup_water',
            'back-up power': 'backup_power',
        })

        # Replace NaN values with NULL
        df.fillna('NULL', inplace=True)
        df.columns = df.columns.str.replace(' ', '_')

        # Clean the 'Price' column
        df['Price'] = df['Price'].apply(lambda x: float(str(x).replace('R', '').replace(' ', '').replace(',', '').replace('\xa0', '')) if "POA" not in str(x) else 0)

        # Query logic
        query = (df['Suburb_Name'] == suburb) & (df['sale_rent'] == rent_sale)
        if min_price not in ["", "any"]:
            query &= (df['Price'].astype(float) >= float(min_price))
        if max_price not in ["", "any"]:
            query &= (df['Price'].astype(float) <= float(max_price))

        filtered_df = df[query]
        print(f'Size of filtered_df after initial filtering: {len(filtered_df)}')

        if filtered_df.empty:
            closest_below = pd.DataFrame()
            closest_above = pd.DataFrame()
            if min_price not in ["", "any"]:
                closest_below = df[(df['Price'].astype(float) < float(min_price)) & (df['Suburb_Name'] == suburb)].nlargest(1, 'Price')
            if max_price not in ["", "any"]:
                closest_above = df[(df['Price'].astype(float) > float(max_price)) & (df['Suburb_Name'] == suburb)].nsmallest(1, 'Price')

            print(f'Size of closest_below: {len(closest_below)}')
            print(f'Size of closest_above: {len(closest_above)}')

            closest_df = pd.concat([closest_below, closest_above], ignore_index=True) if not closest_below.empty and not closest_above.empty else closest_below if not closest_below.empty else closest_above if not closest_above.empty else pd.DataFrame()

            print(f'Size of closest_df: {len(closest_df)}')

            if not closest_df.empty:
                message = ("Although there aren't any property listings within the selected price range, "
                           "we've found some close alternatives that might interest you.")
                filtered_df = closest_df
            else:
                message = "Unfortunately, no records match the given criteria and no close alternatives are available."

        original_filtered_df = filtered_df.copy()

        if back_up_power:
            power_filtered_df = original_filtered_df[original_filtered_df['backup_power'] == 'Yes']
            print(f'Size of power_filtered_df: {len(power_filtered_df)}')
            if power_filtered_df.empty:
                message = "There are currently no property listings with back-up power, but here are other property listings that meet your other criteria"
            else:
                filtered_df = power_filtered_df

        if back_up_water:
            water_filtered_df = original_filtered_df[original_filtered_df['backup_water'] == 'Yes']
            print(f'Size of water_filtered_df: {len(water_filtered_df)}')
            if water_filtered_df.empty:
                message = "There are currently no property listings with back-up water, but here are other property listings that meet your other criteria"
            else:
                filtered_df = water_filtered_df


        # Select only the necessary columns
        selected_columns = [
                'Suburb_Name', 'source_url', 'type_of_property', 'sale_rent',
                'backup_water', 'backup_power', 'Price', 'name',
                'Image', 'garages', 'floor_size', 'erf_size', 'bedrooms',
                'bathrooms'
        ]
        filtered_df = filtered_df[selected_columns]

            # Limit to 4 records
        limited_df = filtered_df.head(4)
        limited_df.reset_index(inplace=True)
        result_dict = limited_df.to_dict('records')


        # Respond with a JSON object containing the results and any message
        response_data = {
            'records': result_dict if not filtered_df.empty else [],
            'message': message if message else ""
        }

        request.session['response_data'] = response_data

        # Store search parameters in session for later use
        search_params = {
            "suburb": suburb,
            "property_type": property_type,
            "rent_sale": rent_sale,
            "min_price": min_price,
            "max_price": max_price,
            "back_up_power": back_up_power,
            "back_up_water": back_up_water
        }

        request.session['search_params'] = search_params

        return redirect('MiBarrioApp:newSearch3')

    return render(request, 'newSearch2.html', {})



@login_required
def new_search_3_view(request):
    if request.method == "POST":
        # Get search parameters from session
        search_params = request.session.get('search_params', {})
        response_data = request.session.get('response_data', {})
        records = response_data.get('records', [])

        print(response_data)
        print(records)

        selected_records = [int(value) for value in request.POST.getlist('save-record')]

        for record_index in selected_records:
            if isinstance(record_index, int):
                record_index = int(record_index)  # Convert to integer
                record_data = records[record_index]  # Get record data by index

                # Create a string representation of the search parameters
                property_search_parameters = ", ".join(f"{key}: {value}" for key, value in search_params.items())

                suburb_instance, created = Suburbs.objects.get_or_create(name=record_data['Suburb_Name'])  # Replace with the correct field for suburb name

                common_properties = {
                    'suburb': suburb_instance,
                    'property_search_parameters': property_search_parameters,
                    'num_of_bedrooms': record_data['bedrooms'],
                    'num_of_bathrooms': record_data['bathrooms'],
                    'has_power_solutions': record_data['backup_power'] == 'Yes',
                    'has_water_solutions': record_data['backup_water'] == 'Yes',
                    'property_type': record_data['type_of_property'],
                }

                sanitized_price = sanitize_price(record_data['Price'])

                if record_data['sale_rent'] == 'sale':
                    property_record = PropertiesToBuy(
                        **common_properties,
                        sale_price=sanitized_price,
                        )
                else:
                    property_record = PropertiesToRent(
                        **common_properties,
                    rental_price=sanitized_price,
                    )

                property_record.save()


            else:
                print(f'Invalid record_index: {record_index}')

        messages.success(request, 'Property listings have been saved successfully!')


    response_data = request.session.get('response_data', {})
    return render(request, 'newSearch3.html', {'response_data': response_data})



@login_required
def view_past_searches_view(request):
    if not request.user.is_authenticated:
        return redirect('MiBarrioApp:login')

    user_searches = Searches.objects.filter(user=request.user).order_by('-search_timestamp')

    past_searches_data = [
        {
            "timestamp": search.search_timestamp,
            "suburb": SearchResult.suburb.name  # Assuming `Suburb` model has a field `name`
        }
        for search in user_searches
        for SearchResult in SearchResults.objects.filter(search=search)
    ]

    # Using Django's paginator
    paginator = Paginator(past_searches_data, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    saved_properties = Properties.objects.filter(user=request.user).order_by('-search_timestamp')

    # Organizing the data in a list of dictionaries (optional, based on your needs)
    saved_properties_data = [
        {
            "suburb": property.suburb.name,  # Assuming suburb is a ForeignKey and has a field name
            "num_of_bedrooms": property.num_of_bedrooms,
            "num_of_bathrooms": property.num_of_bathrooms,
            "has_power_solutions": property.has_power_solutions,
            "has_water_solutions": property.has_water_solutions,
            "property_type": property.property_type,
            "search_timestamp": property.search_timestamp,
            "sale_price": None if not hasattr(property, 'propertiestobuy') else property.propertiestobuy.sale_price,
            "rental_price": None if not hasattr(property, 'propertiestorent') else property.propertiestorent.rental_price,
        }
        for property in saved_properties
    ]

    # Paginating saved properties data
    saved_properties_paginator = Paginator(saved_properties_data, 15)  # Show 15 properties per page
    saved_properties_page_number = request.GET.get('saved_properties_page')
    saved_properties_page_obj = saved_properties_paginator.get_page(saved_properties_page_number)

    # Rendering the template
    return render(request, 'viewPastSearches.html', {
        'page_obj': page_obj,  # Your existing paginated data
        'saved_properties_page_obj': saved_properties_page_obj,  # New paginated data for saved properties
    })

@login_required
def feedback_view(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        category = request.POST.get('category')
        message_text = request.POST.get('message')

        # Assuming the logged in user is `request.user`
        feedback_entry = Feedback(user=request.user, rating=rating, category=category, message=message_text)
        feedback_entry.save()

        messages.success(request, "Feedback successfully submitted!")

        return HttpResponseRedirect(request.path) # This will reload the same feedback page, but now with the success message.

    return render(request, 'feedback.html', {})

def contact_us_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            category = form.cleaned_data['category']
            message = form.cleaned_data['message']

            # Send email
            subject = f"New Contact Form Submission: {category}"
            message = f"Name: {name}\nEmail: {email}\nCategory: {category}\nMessage: {message}"
            from_email = 'mibarrio367@gmail.com'
            recipient_list = ['mibarrio367@gmail.com']
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Add a success message
            messages.success(request, 'Your contact form was successfully submitted.')

            # Redirect to the same page (to clear the form)
            return redirect('MiBarrioApp:contactUs')

    else:
        form = ContactForm()


    return render(request, 'contactUs.html', {'form': form})

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

def sanitize_price(price):
    # Remove any non-numeric characters from price string
    sanitized_price = ''.join(char for char in price if char.isdigit())
    return int(sanitized_price) if sanitized_price else None
