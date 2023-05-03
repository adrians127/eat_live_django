from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from db_app.models import MOMENT_OF_DAY_CHOICES, MealLog
from .forms import AddMealLogForm

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        meal_logs = MealLog.objects.filter(user=request.user.profile, date=timezone.now().date())
        context = {'moment_of_day_choices': MOMENT_OF_DAY_CHOICES,
                   'meal_logs': meal_logs}
        
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