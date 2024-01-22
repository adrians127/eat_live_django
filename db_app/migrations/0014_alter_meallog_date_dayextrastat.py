# Generated by Django 4.2 on 2023-06-18 14:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_profile_activity_level_alter_profile_gender'),
        ('db_app', '0013_alter_meallog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meallog',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 6, 18, 14, 56, 17, 391149, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='DayExtraStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2023, 6, 18, 14, 56, 17, 392149, tzinfo=datetime.timezone.utc))),
                ('water', models.IntegerField(default=0)),
                ('training', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.profile')),
            ],
        ),
    ]