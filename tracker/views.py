from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import timedelta, datetime
from db_app.models import MOMENT_OF_DAY_CHOICES, MealLog, FavouriteProduct, ShoppingProduct, Product
from .forms import AddMealLogForm, UpdateMealLogForm, AddProductForm, AddShoppingProductForm
from calculators.calories_calculator import calculate_nutritions

class Nutritions:
    def __init__(self) -> None:
        self.calories = 0
        self.proteins = 0
        self.fats = 0
        self.carbons = 0

class CalculatedNutritions:
    def __init__(self) -> None:
        self.breakfast = Nutritions()
        self.brunch = Nutritions()
        self.lunch = Nutritions()
        self.snack = Nutritions()
        self.dinner = Nutritions()
        self.all_nutritions = Nutritions()
    
    def round_values(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, Nutritions):
                attr.calories = round(attr.calories, 1)
                attr.proteins = round(attr.proteins, 2)
                attr.fats = round(attr.fats, 2)
                attr.carbons = round(attr.carbons, 2)

@login_required
def calculate_daily_stats(request):
    person = request.user.profile
    person_data = calculate_nutritions(person.weight, person.height, person.age, person.gender, person.activity_level)
    return person_data

def update_nutritions(calculated_nutritions, meal_logs):
    for next in meal_logs:
        product = next.product
        calories = product.calories * ( next.amount / product.portion )
        proteins = product.proteins * ( next.amount / product.portion )
        fats = product.fats * ( next.amount / product.portion )
        carbons = product.carbons * ( next.amount / product.portion )
        match (next.moment_of_day):
            case "BREAKFAST":
                calculated_nutritions.breakfast.calories += calories
                calculated_nutritions.breakfast.proteins += proteins
                calculated_nutritions.breakfast.fats += fats
                calculated_nutritions.breakfast.carbons += carbons
                
            case "BRUNCH":
                calculated_nutritions.brunch.calories += calories
                calculated_nutritions.brunch.proteins += proteins
                calculated_nutritions.brunch.fats += fats
                calculated_nutritions.brunch.carbons += carbons
                
            case "LUNCH":
                calculated_nutritions.lunch.calories += calories
                calculated_nutritions.lunch.proteins += proteins
                calculated_nutritions.lunch.fats += fats
                calculated_nutritions.lunch.carbons += carbons
                
            case "SNACK":
                calculated_nutritions.snack.calories += calories
                calculated_nutritions.snack.proteins += proteins
                calculated_nutritions.snack.fats += fats
                calculated_nutritions.snack.carbons += carbons
                
            case "DINNER":
                calculated_nutritions.dinner.calories += calories
                calculated_nutritions.dinner.proteins += proteins
                calculated_nutritions.dinner.fats += fats
                calculated_nutritions.dinner.carbons += carbons
            case _ :
                raise Exception("error with adding nutritions")

        calculated_nutritions.all_nutritions.calories += calories
        calculated_nutritions.all_nutritions.proteins += proteins
        calculated_nutritions.all_nutritions.fats += fats
        calculated_nutritions.all_nutritions.carbons += carbons

        calculated_nutritions.round_values()

def home(request, date=timezone.now().date()):
    if not request.user.is_authenticated:
        return render(request, 'home.html')
    
    print(type(date))
    meal_logs = MealLog.objects.filter(user=request.user.profile, date = date)
    daily_needs = calculate_daily_stats(request)
    calculated_nutritions = CalculatedNutritions()
    update_nutritions(calculated_nutritions, meal_logs)

    context = {'moment_of_day_choices': MOMENT_OF_DAY_CHOICES,
                'meal_logs': meal_logs,
                'daily_needs': daily_needs,
                'calculated_nutritions': calculated_nutritions,
                'date': date,
                'previous_date': date-timedelta(days=1),
                'next_date': date+timedelta(days=1)}
    
    return render(request, 'home.html', context)

def home_history(request, date):
    if date.endswith('favicon.ico'):
        return HttpResponse(status=204)
    if date == 'add_product':
        return add_product(request)
    if date == 'shopping_list':
        return shopping_list(request)
    if date == 'product_list':
        return product_list(request)
    date_format = "%Y-%m-%d"
    date = datetime.strptime(date.split(' ')[0], date_format).date()
    print(date)
    return home(request, date)


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
    
@login_required
def delete_meal_log(request, meal_log_id):
    print(meal_log_id)
    MealLog.objects.filter(id=meal_log_id).delete()
    return redirect('home')

@login_required
def add_favourite_product(request, meal_log_id):
    FavouriteProduct.objects.create(user=request.user.profile, product=MealLog.objects.get(id=meal_log_id).product)
    return redirect('home')

@login_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            product.save()
            return redirect('add_product')
        return render(request, 'add_product.html', {"form": form})
    else:
        form = AddProductForm()
        return render(request, 'add_product.html', {"form": form})
    
@login_required
def shopping_list(request):
    # Get the current user's shopping products
    shopping_products = ShoppingProduct.objects.filter(user=request.user.profile)

    if request.method == 'POST':
        form = AddShoppingProductForm(request.POST)
        action = request.POST['action']
        if action == 'delete':
            product_ids = request.POST.getlist('product_ids[]')
            ShoppingProduct.objects.filter(id__in=product_ids).delete()
            return redirect('shopping_list')
        if form.is_valid():
            shopping_product = form.save(commit=False)
            shopping_product.user = request.user.profile
            shopping_product.save()
            return redirect('shopping_list')
    else:
        form = AddShoppingProductForm()

    context = {
        'shopping_products': shopping_products,
        'form': form
    }
    return render(request, 'shopping_list.html', context)

# @login_required
# def add_meal_log(request, moment_of_day):
#     if request.method == "POST":
#         form = AddMealLogForm(request.POST)
#         if form.is_valid():

#             meal = form.save(commit=False)
#             meal.user = request.user.profile
#             meal.save()

#             return redirect('home')

#             #nie udało się
#         return render(request, 'add_meal_log.html', {"form": form})
#     else:
#         form = AddMealLogForm()
#         form.fields['moment_of_day'].initial = moment_of_day
#         return render(request, 'add_meal_log.html', {"form": form, "moment_of_day": moment_of_day})

@login_required
def add_meal_log(request, moment_of_day):
    query = request.GET.get('search')
    min_calories = request.GET.get('min_calories')
    max_calories = request.GET.get('max_calories')
    min_proteins = request.GET.get('min_proteins')
    max_proteins = request.GET.get('max_proteins')
    min_fats = request.GET.get('min_fats')
    max_fats = request.GET.get('max_fats')
    min_carbons = request.GET.get('min_carbons')
    max_carbons = request.GET.get('max_carbons')

    user = request.user.profile
    favourite_products = Product.objects.filter(favouriteproduct__user = user)
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
        favourite_products = favourite_products.filter(name__icontains=query)

    if min_calories:
        products = products.filter(calories__gte=min_calories)
        favourite_products = favourite_products.filter(calories__gte=min_calories)
    if max_calories:
        products = products.filter(calories__lte=max_calories)
        favourite_products = favourite_products.filter(calories__lte=max_calories)

    if min_proteins:
        products = products.filter(proteins__gte=min_proteins)
        favourite_products = favourite_products.filter(proteins__gte=min_proteins)
    if max_proteins:
        products = products.filter(proteins__lte=max_proteins)
        favourite_products = favourite_products.filter(proteins__lte=max_proteins)

    if min_fats:
        products = products.filter(fats__gte=min_fats)
        favourite_products = favourite_products.filter(fats__gte=min_fats)
    if max_fats:
        products = products.filter(fats__lte=max_fats)
        favourite_products = favourite_products.filter(fats__lte=max_fats)

    if min_carbons:
        products = products.filter(carbons__gte=min_carbons)
        favourite_products = favourite_products.filter(carbons__gte=min_carbons)
    if max_carbons:
        products = products.filter(carbons__lte=max_carbons)
        favourite_products = favourite_products.filter(carbons__lte=max_carbons)


    if request.method == "POST":
        form = AddMealLogForm(request.POST)
        print(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user.profile
            meal.save()
            return redirect('home')
        else:
            return render(request, 'add_meal_log.html', {"form": form, "moment_of_day": moment_of_day, "products": products, 'favourite_products': favourite_products})
    else:
        form = AddMealLogForm()
        form.fields['moment_of_day'].initial = moment_of_day
        form.fields['date'].initial = timezone.now().date()
        return render(request, 'add_meal_log.html', {"form": form, "moment_of_day": moment_of_day, "products": products, 'favourite_products': favourite_products})


@login_required
def product_list(request):
    query = request.GET.get('search')
    min_calories = request.GET.get('min_calories')
    max_calories = request.GET.get('max_calories')
    min_proteins = request.GET.get('min_proteins')
    max_proteins = request.GET.get('max_proteins')
    min_fats = request.GET.get('min_fats')
    max_fats = request.GET.get('max_fats')
    min_carbons = request.GET.get('min_carbons')
    max_carbons = request.GET.get('max_carbons')

    user = request.user.profile
    favourite_products = Product.objects.filter(favouriteproduct__user = user)

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
        favourite_products = favourite_products.filter(name__icontains=query)

    if min_calories:
        products = products.filter(calories__gte=min_calories)
        favourite_products = favourite_products.filter(calories__gte=min_calories)
    if max_calories:
        products = products.filter(calories__lte=max_calories)
        favourite_products = favourite_products.filter(calories__lte=max_calories)

    if min_proteins:
        products = products.filter(proteins__gte=min_proteins)
        favourite_products = favourite_products.filter(proteins__gte=min_proteins)
    if max_proteins:
        products = products.filter(proteins__lte=max_proteins)
        favourite_products = favourite_products.filter(proteins__lte=max_proteins)

    if min_fats:
        products = products.filter(fats__gte=min_fats)
        favourite_products = favourite_products.filter(fats__gte=min_fats)
    if max_fats:
        products = products.filter(fats__lte=max_fats)
        favourite_products = favourite_products.filter(fats__lte=max_fats)

    if min_carbons:
        products = products.filter(carbons__gte=min_carbons)
        favourite_products = favourite_products.filter(carbons__gte=min_carbons)
    if max_carbons:
        products = products.filter(carbons__lte=max_carbons)
        favourite_products = favourite_products.filter(carbons__lte=max_carbons)

    return render(request, 'product_list.html', {'products': products,
                                                 'favourite_products': favourite_products})
