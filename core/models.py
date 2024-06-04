from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', verbose_name='Фото пользователя', blank=True, null=True)
    email = models.EmailField()
    phone = PhoneNumberField(verbose_name='Телефонный номер', blank=True, null=True)

    def __str__(self):
        return self.username


# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    background = models.ImageField(upload_to='backgrounds/', verbose_name='Фон страницы', blank=True,
                                   null=True)

    menu = models.CharField(max_length=100, verbose_name='меню')
    content = RichTextField()
    active = models.BooleanField(default=False, verbose_name='актив')
    create_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True, blank=True)

    def __str__(self):
        return self.menu
