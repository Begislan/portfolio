from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('core.urls')),
    # auth
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("accounts/", include("accounts.urls")),  # new
    # admin
    path('adminka/', include('adminka.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)