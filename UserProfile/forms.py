# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.safestring import mark_safe

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label=mark_safe("<strong> Email (will be used as Username) </strong>"),
                             max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'enter a valid email address', 'class': 'form-control'}))
    password1 = forms.CharField(label=mark_safe("<strong> Choose Password </strong>"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'please enter password', 'class': 'form-control'}))
    password2 = forms.CharField(label=mark_safe("<strong> Confirm Password </strong>"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'please confirm password', 'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'enter your phone number', 'class': 'form-control'}))  # New field

    class Meta(UserCreationForm):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2']

class UserEditForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))  # New field

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'picture']
