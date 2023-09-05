from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SearchProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class SearchProfileForm(forms.ModelForm):
    class Meta:
        model = SearchProfile
        fields = ['sp_name', 'age', 'social_cultural', 'health_wellness',
                  'leisure_recreation', 'community_services',
                  'transportation_active', 'transportation_public',
                  'backup_power_supply', 'backup_water_supply']
