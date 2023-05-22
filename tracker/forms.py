from django import forms
from db_app.models import MealLog, Product, ShoppingProduct, Recipe


class AddMealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['product', 'amount', 'moment_of_day', 'date']

class UpdateMealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['moment_of_day', 'product', 'amount']

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'calories', 'proteins', 'fats', 'carbons', 'portion']

class AddShoppingProductForm(forms.ModelForm):
    class Meta:
        model = ShoppingProduct
        fields = ['product', 'amount']