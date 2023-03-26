from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def calculators(request):
    return render(request, 'calculators/calculators.html')