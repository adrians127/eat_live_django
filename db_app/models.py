from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import date
from members.models import Profile

BREAKFAST = 'BREAKFAST'
BRUNCH = 'BRUNCH'
LUNCH = 'LUNCH'
SNACK = 'SNACK'
DINNER = 'DINNER'


MOMENT_OF_DAY_CHOICES = [
    (BREAKFAST, 'Breakfast'),
    (BRUNCH, 'Brunch'),
    (LUNCH, 'Lunch'),
    (SNACK, 'Snack'),
    (DINNER, 'Dinner')
]


class Product(models.Model):
    name = models.CharField(max_length=100)
    calories = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    proteins = models.FloatField(default=0, validators=[MinValueValidator(0)])
    fats = models.FloatField(default=0, validators=[MinValueValidator(0)])
    carbons = models.FloatField(default=0, validators=[MinValueValidator(0)])
    portion = models.IntegerField(default=100, validators=[MinValueValidator(0)]) #100g

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default="No description")

    def __str__(self):
        return self.name

class RecipeDetail(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.recipe) + "-" + str(self.product)

class MealLog(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now())
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    moment_of_day = models.CharField(max_length=15, choices=MOMENT_OF_DAY_CHOICES)

    def __str__(self):
        return str(self.user) + " - " + str(self.date) + " - " + str(self.moment_of_day)

class FavouriteProduct(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " " + str(self.product)

class ShoppingProduct(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user) + " " + str(self.product) + " " + str(self.amount)