# accounts/urls.py
from django.urls import path, include

from . import views
from .views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('logout/', views.logout_view, name='logout'),

]
