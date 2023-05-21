from django import forms
from db_app.models import MealLog, Product, ShoppingProduct

# class AddMealLogForm(forms.ModelForm):
#     favorite_product = forms.ModelChoiceField(
#         label='Choose from favorite products',
#         queryset=FavouriteProduct.objects.none(),
#         required=False
#     )
#     # all_products = forms.ModelChoiceField(
#     #     label='Choose from all products',
#     #     queryset=Product.objects.all()
#     # )

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(AddMealLogForm, self).__init__(*args, **kwargs)
#         self.fields['favorite_product'].queryset = self.get_favorite_products(user)
#         # self.fields['all_products'].queryset = Product.objects.all()

#     def get_favorite_products(self, user):
#         if user:
#             return FavouriteProduct.objects.filter(user=user).values_list('product')
#         return []

#     class Meta:
#         model = MealLog
#         fields = ['favorite_product', 'amount', 'moment_of_day']


class AddMealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['product', 'amount', 'moment_of_day', 'date']

class UpdateMealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['moment_of_day', 'product', 'amount']

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'calories', 'proteins', 'fats', 'carbons', 'portion']

class AddShoppingProductForm(forms.ModelForm):
    class Meta:
        model = ShoppingProduct
        fields = ['product', 'amount']