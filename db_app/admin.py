from django.contrib import admin
from .models import Product, Recipe, RecipeDetail, MealLog, FavouriteProduct, ShoppingProduct

admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(RecipeDetail)
admin.site.register(MealLog)
admin.site.register(FavouriteProduct)
admin.site.register(ShoppingProduct)