from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home, name='home'),
    path('add_meal/<str:moment_of_day>/', views.add_meal_log, name='add_meal'),
    path('update_meal/<int:meal_log_id>/', views.update_meal_log, name='update_meal'),
    path('delete_meal/<int:meal_log_id>/', views.delete_meal_log, name='delete_meal')
]