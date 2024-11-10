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
    ost_name = models.CharField(max_length=255, verbose_name='отечество', blank=True, null=True)
    phone = PhoneNumberField(verbose_name='Телефонный номер', blank=True, null=True, help_text="Введите номер телефона в формате: +123456789")

    def save(self, *args, **kwargs):
        # Проверяем, есть ли фото и не закрыт ли файл
        if self.photo and not self.photo.closed:
            img = Image.open(self.photo)
            output = BytesIO()

            # Получаем текущие размеры изображения
            original_width, original_height = img.size

            # Проверяем формат изображения (PNG или JPEG)
            image_format = img.format

            # Если изображение превышает 300x300, изменяем его размер
            if original_width > 300 or original_height > 300:
                # Сохраняем пропорции изображения
                aspect_ratio = original_width / original_height

                if original_width > original_height:
                    new_width = 300
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = 300
                    new_width = int(new_height * aspect_ratio)

                # Изменяем размер изображения
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Проверяем, если изображение в формате PNG, и оно содержит альфа-канал (прозрачность)
            if image_format == 'PNG' and img.mode in ('RGBA', 'LA'):
                img = img.convert('RGBA')  # Сохраняем альфа-канал
                img.save(output, format='PNG')  # Сохраняем как PNG
                mime_type = 'image/png'
            else:
                # Конвертируем все остальные форматы в RGB для сохранения в JPEG
                img = img.convert('RGB')
                img.save(output, format='JPEG', quality=85)
                mime_type = 'image/jpeg'

            output.seek(0)

            # Меняем значение поля photo на новое измененное изображение
            self.photo = InMemoryUploadedFile(
                output, 'ImageField', self.photo.name, mime_type, sys.getsizeof(output), None
            )

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



def resize_image(image, max_height=800, quality=85):
    img = Image.open(image)

    # Определяем исходный формат изображения
    image_format = img.format

    # Проверяем, если изображение в режиме RGBA (имеет альфа-канал), конвертируем в RGB
    if img.mode in ('RGBA', 'LA'):
        img = img.convert('RGB')

    # Получаем текущие размеры изображения
    original_width, original_height = img.size

    # Если высота превышает max_height, пересчитываем ширину
    if original_height > max_height:
        aspect_ratio = original_width / original_height
        new_height = max_height
        new_width = int(new_height * aspect_ratio)
    else:
        # Если исходная высота меньше max_height, сохраняем оригинальные размеры
        new_width, new_height = original_width, original_height

    # Изменяем размер изображения, сохраняя соотношение сторон
    img = img.resize((new_width, new_height), Image.LANCZOS)

    # Подготавливаем буфер для сохранения изображения
    output = BytesIO()

    # Сохраняем изображение в исходном формате
    if image_format == 'PNG':
        img.save(output, format='PNG')
        mime_type = 'image/png'
    else:
        img.save(output, format='JPEG', quality=quality)
        mime_type = 'image/jpeg'

    output.seek(0)

    # Возвращаем InMemoryUploadedFile
    return InMemoryUploadedFile(
        output, 'ImageField', f"{image.name.split('.')[0]}.{image_format.lower()}", mime_type,
        sys.getsizeof(output), None
    )


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