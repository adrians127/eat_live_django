from django.shortcuts import render
from django.utils import timezone
from db_app.models import MOMENT_OF_DAY_CHOICES, MealLog

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        meal_logs = MealLog.objects.filter(user=request.user.profile, date=timezone.now().date())
        context = {'moment_of_day_choices': MOMENT_OF_DAY_CHOICES,
                   'meal_logs': meal_logs}
        
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')