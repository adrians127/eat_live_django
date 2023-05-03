from django import forms
from db_app.models import MealLog

class AddMealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['product', 'amount', 'moment_of_day']