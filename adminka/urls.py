from django.urls import path
from .views import *

urlpatterns = [
    path('', admin_core, name='admin_core'),
    path('adm/<int:id>/', admin_portfolio_detail, name='admin_portfolio_detail'),
    path('create/', portfolio_create_view, name='create_portfolio'),
    path('/update/<int:pk>/', portfolio_update_view, name='portfolio_update'),
    path('/delete/<int:pk>/', portfolio_delete_view, name='portfolio_delete'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
]
