from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import Portfolio

# Register your models here.

admin.site.register(Portfolio)

admin.site.register(CustomUser)