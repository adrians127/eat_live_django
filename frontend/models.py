from django.db import models

# Create your models here.
class CalculationForm(models.Model):
    age = models.IntegerField()
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=20)

class LoginForm(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=40)

class RegisterForm(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=40)
    repeatPassword = models.CharField(max_length=40)