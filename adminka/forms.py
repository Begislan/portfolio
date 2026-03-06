# forms.py
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from core.models import Portfolio
from core.models import CustomUser

class PortfolioForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Portfolio
        fields = ['menu', 'content', 'active', 'background']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo', 'phone']