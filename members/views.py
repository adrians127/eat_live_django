from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreateLoginForm, RegisterUserForm, UpdateUserForm, UpdateProfileForm

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
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            #obsługa rejestracji
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_update')
            
            #nie udało się
            info = "The registration was unsuccessful"
            return render(request, 'register.html', {"form": form, "info":info})
        else:
            info = "The password is not strong enough"
            return render(request, 'register.html', {"form": form, "info": info})
    else:
        form = RegisterUserForm()
        return render(request, 'register.html', {"form": form})

@login_required
def user_page(request):
    return render(request, 'user_home.html')

@login_required
def user_update_page(request):
    if request.method == "POST":
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('userpage')
        
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user_update.html', context)