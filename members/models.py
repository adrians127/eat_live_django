from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
ACTIVITY_LVL_CHOICES = [
    (1.2, 'No physical activity'),
    (1.4, 'Low physical activity (140 minutes per week)'),
    (1.6, 'Medium physical activity (280 minutes per week)'),
    (1.8, 'High physical activity (420 minutes per week)'),
    (2.0, 'Very high physical activity (560 minutes per week)')
]
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(default='')
    gender = models.CharField(max_length=10, default='O', choices=GENDER_CHOICES)
    age = models.IntegerField(default=21)
    weight = models.FloatField(default=60)
    height = models.IntegerField(default=170)
    activity_level = models.FloatField(default=1.2, choices=ACTIVITY_LVL_CHOICES)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()