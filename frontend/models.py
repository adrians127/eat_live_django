from django.db import models

# Create your models here.
class CalculationForm(models.Model):
    age = models.IntegerField()
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=20)