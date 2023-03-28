from django import forms

class CreateCalculationForm(forms.Form):
    age = forms.IntegerField(label="Age", max_value=130, min_value=15)
    weight = forms.IntegerField(label="Weight", max_value=500, min_value=20)
    height = forms.IntegerField(label="Height", max_value=300, min_value=100)
    gender = forms.CharField(label="Gender", max_length=20)