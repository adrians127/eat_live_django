from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import timedelta, datetime
from db_app.models import MOMENT_OF_DAY_CHOICES, MealLog, FavouriteProduct
from .forms import AddMealLogForm, UpdateMealLogForm, AddProductForm
from calculators.calories_calculator import calculate_nutritions
from members.models import Profile
import re


class Nutritions:
    def __init__(self) -> None:
        self.calories = 0
        self.proteins = 0
        self.fats = 0
        self.carbons = 0

class CalculatedNutritions:
    def __init__(self) -> None:
        self.breakfast = Nutritions()
        self.brunch = Nutritions()
        self.lunch = Nutritions()
        self.snack = Nutritions()
        self.dinner = Nutritions()
        self.all_nutritions = Nutritions()
    
    def round_values(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Nutritions):
                attr.calories = round(attr.calories, 1)
                attr.proteins = round(attr.proteins, 2)
                attr.fats = round(attr.fats, 2)
                attr.carbons = round(attr.carbons, 2)

@login_required
def calculate_daily_stats(request):
    person = request.user.profile
    person_data = calculate_nutritions(person.weight, person.height, person.age, person.gender, person.activity_level)
    return person_data

def update_nutritions(calculated_nutritions, meal_logs):
    for next in meal_logs:
        product = next.product
        calories = product.calories * ( next.amount / product.portion )
        proteins = product.proteins * ( next.amount / product.portion )
        fats = product.fats * ( next.amount / product.portion )
        carbons = product.carbons * ( next.amount / product.portion )
        match (next.moment_of_day):
            case "BREAKFAST":
                calculated_nutritions.breakfast.calories += calories
                calculated_nutritions.breakfast.proteins += proteins
                calculated_nutritions.breakfast.fats += fats
                calculated_nutritions.breakfast.carbons += carbons
                
            case "BRUNCH":
                calculated_nutritions.brunch.calories += calories
                calculated_nutritions.brunch.proteins += proteins
                calculated_nutritions.brunch.fats += fats
                calculated_nutritions.brunch.carbons += carbons
                
            case "LUNCH":
                calculated_nutritions.lunch.calories += calories
                calculated_nutritions.lunch.proteins += proteins
                calculated_nutritions.lunch.fats += fats
                calculated_nutritions.lunch.carbons += carbons
                
            case "SNACK":
                calculated_nutritions.snack.calories += calories
                calculated_nutritions.snack.proteins += proteins
                calculated_nutritions.snack.fats += fats
                calculated_nutritions.snack.carbons += carbons
                
            case "DINNER":
                calculated_nutritions.dinner.calories += calories
                calculated_nutritions.dinner.proteins += proteins
                calculated_nutritions.dinner.fats += fats
                calculated_nutritions.dinner.carbons += carbons
            case _ :
                raise Exception("error with adding nutritions")

        calculated_nutritions.all_nutritions.calories += calories
        calculated_nutritions.all_nutritions.proteins += proteins
        calculated_nutritions.all_nutritions.fats += fats
        calculated_nutritions.all_nutritions.carbons += carbons

        calculated_nutritions.round_values()

def home(request, date=timezone.now().date()):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    
    print(type(date))
    meal_logs = MealLog.objects.filter(user=request.user.profile, date = date)
    data = calculate_daily_stats(request)
    calculated_nutritions = CalculatedNutritions()
    update_nutritions(calculated_nutritions, meal_logs)

    context = {'moment_of_day_choices': MOMENT_OF_DAY_CHOICES,
                'meal_logs': meal_logs,
                'data': data,
                'calculated_nutritions': calculated_nutritions,
                'date': date,
                'previous_date': date-timedelta(days=1),
                'next_date': date+timedelta(days=1)}
    
    return render(request, 'home.html', context)

def home_history(request, date):
    if date.endswith('favicon.ico'):
        return HttpResponse(status=204)
    if date == 'add_product':
        return add_product(request)
    date_format = "%Y-%m-%d"
    date = datetime.strptime(date.split(' ')[0], date_format).date()
    print(date)
    return home(request, date)


@login_required
def add_meal_log(request, moment_of_day):
    if request.method == "POST":
        form = AddMealLogForm(request.POST)
        if form.is_valid():

            meal = form.save(commit=False)
            meal.user = request.user.profile
            meal.save()

            return redirect('home')

            #nie udało się
        return render(request, 'add_meal_log.html', {"form": form})
    else:
        form = AddMealLogForm()
        form.fields['moment_of_day'].initial = moment_of_day
        return render(request, 'add_meal_log.html', {"form": form, "moment_of_day": moment_of_day})

@login_required
def update_meal_log(request, meal_log_id):
    meal_log = MealLog.objects.get(id=meal_log_id)
    if request.method == "POST":
        form = UpdateMealLogForm(request.POST, instance=meal_log)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UpdateMealLogForm(instance=meal_log)
        return render(request, "update_meal_log.html", {"form": form, "meal_log": meal_log})
    
@login_required
def delete_meal_log(meal_log_id):
    MealLog.objects.filter(id=meal_log_id).delete()
    return redirect('home')

@login_required
def add_favourite_product(request, meal_log_id):
    FavouriteProduct.objects.create(user=request.user.profile, product=MealLog.objects.get(id=meal_log_id).product)
    return redirect('home')

@login_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            product.save()
            return redirect('add_product')
        return render(request, 'add_product.html', {"form": form})
    else:
        form = AddProductForm()
        return render(request, 'add_product.html', {"form": form})