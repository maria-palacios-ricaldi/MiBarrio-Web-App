from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


CATEGORY_CHOICES = [
    ('Bug Report', 'Bug Report'),
    ('Feature Request', 'Feature Request'),
    ('General Inquiry', 'General Inquiry'),
    ('Technical Support', 'Technical Support'),
    ('Other', 'Other'),
]

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    category = forms.ChoiceField(
    widget=forms.Select(attrs={'class': 'category-dropdown'}),
    choices=CATEGORY_CHOICES
)

    message = forms.CharField(
    widget=forms.Textarea(attrs={'rows': 4}) 
)
