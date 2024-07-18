from django.contrib.auth.forms import UserCreationForm
from core.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'first_name','ost_name', 'last_name', 'email','phone', 'photo')

