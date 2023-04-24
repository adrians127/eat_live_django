# Generated by Django 4.2 on 2023-04-24 22:43

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_profile_activity_level_alter_profile_gender'),
        ('db_app', '0002_recipe_recipedetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2023, 4, 25))),
                ('amount', models.IntegerField(default=0)),
                ('moment_of_day', models.CharField(choices=[('BREAKFAST', 'Breakfast'), ('BRUNCH', 'Brunch'), ('LUNCH', 'Lunch'), ('SNACK', 'Snack'), ('DINNER', 'Dinner')], max_length=15)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.profile')),
            ],
        ),
    ]