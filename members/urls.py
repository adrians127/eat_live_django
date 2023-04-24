from django.urls import path
from . import views
urlpatterns = [ 
    path('login/', views.login_user),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('userpage/', views.user_page, name='userpage'),
    path('userpage/update', views.user_update_page, name="user_update")
]
