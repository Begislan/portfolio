from django.urls import path
from .views import core, user

urlpatterns = [
    path('', core, name='core'),
    path('user/<str:username>/', user, name='user'),
]