# users/signals.py

# django
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

# local
from . models import UserProfile

# signal receiver on new user to create userprofile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
  if created:
    obj, created = UserProfile.objects.get_or_create(user=instance)