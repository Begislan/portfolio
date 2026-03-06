# accounts/urls.py
from django.urls import path, include

from . import views
from .views import SignUpView, login_user

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('login/', login_user, name='login')

]
