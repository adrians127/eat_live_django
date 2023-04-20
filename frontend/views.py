from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CreateCalculationForm, CreateLoginForm, CreateRegisterForm
from .models import CalculationForm, LoginForm
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

def login(response):
    if response.method == "POST":
        form = CreateLoginForm(response.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            #obsługa logowania
            # ...

            #udało się
            info = "You successfully logged in!"


            #nie udało się
            # info = "Incorrect email or password. Try again"
            return render(response, 'login.html', {"form": form, "info":info})
    else:
        form = CreateLoginForm()
    return render(response, 'login.html', {"form": form})

def register(response):
    if response.method == "POST":
        form = CreateRegisterForm(response.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            repeatPassword = form.cleaned_data["repeatPassword"]

            #obsługa rejestracji
            # ...

            #udało się
            info = "You successfully registered!"


            #nie udało się
            # info = "The registration was unsuccessful"
            return render(response, 'register.html', {"form": form, "info":info})
    else:
        form = CreateRegisterForm()
    return render(response, 'register.html', {"form": form})