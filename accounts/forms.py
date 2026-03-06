from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name','ost_name', 'last_name', 'email','phone', 'photo')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
