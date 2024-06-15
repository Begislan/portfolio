# forms.py
from django import forms
from core.models import Portfolio
from core.models import CustomUser

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['background', 'menu', 'content', 'active']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo', 'phone']