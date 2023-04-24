from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCalculationForm
from calculators.bmi_calculator import calculate_bmi
from calculators.water_calculator import water_calculate
from calculators.calories_calculator import calculate_nutritions


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
            activity_lvl = float(form.cleaned_data["activity_lvl"])
            content = (calculate_bmi(weight, height), water_calculate(
                age, gender), calculate_nutritions(weight, height, age, gender, activity_lvl))

        return render(response, 'calculators.html', {"form": form, 'content': content})

    else:
        form = CreateCalculationForm()
        return render(response, 'calculators.html', {"form": form})