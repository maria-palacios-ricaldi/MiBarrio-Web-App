from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *

app_name = "MiBarrioApp"

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('home/', views.home_view, name='home'),
    #path('register/', auth_views.LoginView.as_view(template_name='register.html'), name='register'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
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
    path('viewPastSearches', views.view_past_searches_view, name = "viewPastSearches"),
    path('feedback', views.feedback_view, name ="feedback" ),
    path('contactUs', views.contact_us_view, name='contactUs'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
