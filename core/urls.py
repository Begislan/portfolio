from django.urls import path
from .views import core, user, list_portfolios

urlpatterns = [
    path('', core, name='core'),
    path('user/<str:username>/', user, name='user'),
    path('list-portfolios', list_portfolios, name='list_portfolios')
]