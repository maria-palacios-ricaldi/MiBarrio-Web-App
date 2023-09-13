from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import *

app_name = "MiBarrioApp"

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('home/', views.home_view, name='home'),
    #path('register/', auth_views.LoginView.as_view(template_name='register.html'), name='register'),
    path('register/', views.register, name='register'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # password control
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name="change-password"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html', subject_template_name='password_reset_subject.txt', html_email_template_name='password_reset_email.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    #other web app pages
    path('aboutUs', views.about_us_view, name ='aboutUs'),
    path('profile', views.profile_view, name = "profile"),
    path('newSearch', views.new_search_view, name = "newSearch"),
    path('newSearch2', views.new_search_2_view, name = "newSearch2"),
    path('newSearch3', views.new_search_3_view, name = "newSearch3"),
    path('viewPastSearches', views.view_past_searches_view, name = "viewPastSearches"),
    path('feedback', views.feedback_view, name ="feedback" ),
    path('contactUs', views.contact_us_view, name='contactUs'),
    path('test', views.test_view, name='test'),

    #AJAX related:
    path('get_nearest_suburbs/', views.get_nearest_suburbs, name='get_nearest_suburbs'),
    path('get_crime_data/<str:suburb_name>/', views.get_crime_data, name='get_crime_data'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
