from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import CalculationForm
from .forms import CreateCalculationForm
from calculators.bmi_calculator import calculate_bmi
from calculators.water_calculator import water_calculate
from calculators.calories_calculator import calculate_nutritions

# Create your views here.


def home(request):
    return render(request, 'home.html')


def calculators(response):
    if response.method == "POST":
        form = CreateCalculationForm(response.POST)
        if form.is_valid():
            age = form.cleaned_data["age"]
            weight = form.cleaned_data["weight"]
            height = form.cleaned_data["height"]
            gender = form.cleaned_data["gender"]
            input = CalculationForm(
                age=age, weight=weight, height=height, gender=gender)
            content = (calculate_bmi(input.weight, input.height), water_calculate(
                input.age, input.gender), calculate_nutritions(input.weight, input.height, input.age, input.gender))

        return render(response, 'calculators.html', {"form": form, 'content': content})

    else:
        form = CreateCalculationForm()
        return render(response, 'calculators.html', {"form": form})