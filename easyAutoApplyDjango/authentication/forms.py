# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import your CustomUser model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'wix_id')  # Add the fields you want in the registration form
