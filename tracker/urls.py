from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home, name='home'),
    path('add_meal/<str:moment_of_day>/', views.add_meal_log, name='add_meal')
]