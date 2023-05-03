from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from db_app.models import MOMENT_OF_DAY_CHOICES, MealLog
from .forms import AddMealLogForm, UpdateMealLogForm
from calculators.calories_calculator import calculate_nutritions
from members.models import Profile

@login_required
def calculate_daily_stats(request):
    # meal_logs = MealLog.objects.filter(user=request.user.profile, date=timezone.now().date())
    person = request.user.profile
    person_data = calculate_nutritions(person.weight, person.height, person.age, person.gender, person.activity_level)
    # person_data = calculate_calories(60, 170, 20, 'M', 1.2)
    return person_data

def home(request):
    if request.user.is_authenticated:
        meal_logs = MealLog.objects.filter(user=request.user.profile, date=timezone.now().date())
        data = calculate_daily_stats(request)
        # data = (20, 20)
        context = {'moment_of_day_choices': MOMENT_OF_DAY_CHOICES,
                   'meal_logs': meal_logs,
                   'data': data}
        
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')

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