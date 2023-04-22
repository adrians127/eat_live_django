from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateLoginForm, RegisterUserForm

# Create your views here.

def login_user(request):
    if request.method == "POST":
        form = CreateLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            #obsługa logowania
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

            #nie udało się
            info = "The logging in was unsuccessful"
            return render(request, 'login.html', {"form": form, "info":info})
    else:
        form = CreateLoginForm()
        return render(request, 'login.html', {"form": form})

def logout_user(request):
    logout(request)
    messages.success(request, ("You successfully logged out!"))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            # first_name = form.cleaned_data["first_name"]

            #obsługa rejestracji
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You successfully registered!")
                return redirect('home')
            
            #nie udało się
            info = "The registration was unsuccessful"
            return render(request, 'register.html', {"form": form, "info":info})
        else:
            messages.error(request, "The password is not strong enough")
            return render(request, 'register.html', {"form": form})
    else:
        form = RegisterUserForm()
        return render(request, 'register.html', {"form": form})