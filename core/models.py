from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField

from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', verbose_name='Фото пользователя', blank=True, null=True)
    email = models.EmailField()
    phone = PhoneNumberField(verbose_name='Телефонный номер', blank=True, null=True, help_text="Введите номер телефона в формате: +123456789")

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

# Signals
@receiver(post_save, sender=CustomUser)
def create_initial_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance, menu='Резюме', content='Content for Menu 1', active=True)
        Portfolio.objects.create(user=instance, menu='Биография', content='Content for Menu 2', active=True)
        Portfolio.objects.create(user=instance, menu='Жетишкендиктер', content='Content for Menu 3', active=True)
