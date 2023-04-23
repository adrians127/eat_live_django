from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from members.models import GENDER_CHOICES, ACTIVITY_LVL_CHOICES

class CreateLoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=40)
    password = forms.CharField(label="Password", max_length=40, widget=forms.PasswordInput())

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    gender = forms.ChoiceField(label="Gender", widget=forms.RadioSelect, choices=GENDER_CHOICES)
    activity_lvl = forms.ChoiceField(label="Activity level (PAL)", widget=forms.RadioSelect, choices=ACTIVITY_LVL_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')