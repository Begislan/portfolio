from django.urls import path
from .views import admin_core

urlpatterns = [
    path('', admin_core, name='admin_core')
]