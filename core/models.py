from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from io import BytesIO
from django.db.models.signals import pre_save
from bs4 import BeautifulSoup
import requests
from django.core.files.base import ContentFile
import os
from urllib.parse import urlparse
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', verbose_name='Фото пользователя', blank=True, null=True)
    email = models.EmailField()
    ost_name = models.CharField(max_length=255, verbose_name='отечество', default="без отечество")
    phone = PhoneNumberField(verbose_name='Телефонный номер', blank=True, null=True, help_text="Введите номер телефона в формате: +123456789")

    def save(self, *args, **kwargs):
        # Проверяем, есть ли фото и не закрыт ли файл
        if self.photo and not self.photo.closed:
            img = Image.open(self.photo)
            output = BytesIO()

            # Изменяем размер изображения (вы можете изменить размер)
            img = img.resize((300, 300), Image.LANCZOS)

            # Сохраняем измененное изображение в output
            img.save(output, format='JPEG', quality=85)
            output.seek(0)

            # Меняем значение поля photo на новое измененное изображение
            self.photo = InMemoryUploadedFile(output, 'ImageField',
                                              self.photo.name, 'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)

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
        Portfolio.objects.create(user=instance, menu='Успехи', content='Content for Menu 3', active=True)
        Portfolio.objects.create(user=instance, menu='Образование', content='Content for Menu 3', active=True)
        Portfolio.objects.create(user=instance, menu='Трудовая деятельность', content='Content for Menu 3', active=True)
        Portfolio.objects.create(user=instance, menu='Наука', content='Content for Menu 3', active=True)


def resize_image(image, size=(800, 800), quality=85):
    img = Image.open(image)
    img = img.convert('RGB')
    img = img.resize(size, Image.LANCZOS)
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', f"{image.name.split('.')[0]}.jpg", 'image/jpeg',
                                sys.getsizeof(output), None)


@receiver(pre_save, sender=Portfolio)
def resize_images_in_content(sender, instance, **kwargs):
    soup = BeautifulSoup(instance.content, 'html.parser')
    for img in soup.find_all('img'):
        image_url = img['src']
        if image_url.startswith('http'):
            response = requests.get(image_url)
            if response.status_code == 200:
                image_content = ContentFile(response.content)
                resized_image = resize_image(image_content)
                image_name = os.path.basename(urlparse(image_url).path)
                img['src'] = f"data:image/jpeg;base64,{resized_image.read().encode('base64')}"

    instance.content = str(soup)