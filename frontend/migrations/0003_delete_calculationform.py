# Generated by Django 4.2 on 2023-04-23 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_delete_loginform_delete_registerform'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CalculationForm',
        ),
    ]