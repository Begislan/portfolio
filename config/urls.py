from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

from django.contrib.sitemaps.views import sitemap






urlpatterns = [
    path('admin/', admin.site.urls),

    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('', include('core.urls')),
    # auth
    path("accounts/", include("accounts.urls")),  # new
    # admin
    path('adm/', include('adminka.urls')),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)