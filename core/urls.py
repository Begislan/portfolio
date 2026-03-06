from django.urls import path
from .views import core, user, list_portfolios, delete_user
from core import views

urlpatterns = [
    path('', core, name='core'),
    path('user/<str:username>/', user, name='user'),
    path('list-portfolios', list_portfolios, name='list_portfolios'),
    path('delete-portfolio/<str:username>/', delete_user, name='delete_user'),
    path("portfolio/<int:pk>/pdf/", views.portfolio_pdf, name="portfolio_pdf")

]
