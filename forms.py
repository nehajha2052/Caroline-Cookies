from django import forms
from .models import User, Purchases, Products, ProductReviews
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from .views import *


class CustomUserCreationForm(UserCreationForm):
    """Registration form."""

    class Meta:
        
     model = User
     fields = ("email", "password", "first_name", "last_name", "date_of_birth", "address",)
     widgets = {
         'email': forms.TextInput(attrs={"class": "form-control"}),
         'password': forms.TextInput(attrs={"class": "form-control"}),
         'first_name': forms.TextInput(attrs={"class": "form-control"}),
         'last_name': forms.TextInput(attrs={"class": "form-control"}),
         'date_of_birth': forms.TextInput(attrs={"class": "form-control"}),
         'address': forms.TextInput(attrs={"class": "form-control"}),

     }
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
     