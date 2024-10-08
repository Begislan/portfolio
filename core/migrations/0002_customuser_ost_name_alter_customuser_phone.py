# Generated by Django 5.0.6 on 2024-07-08 04:51

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ost_name',
            field=models.CharField(default='без отечество', max_length=255, verbose_name='отечество'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Введите номер телефона в формате: +123456789', max_length=128, null=True, region=None, verbose_name='Телефонный номер'),
        ),
    ]