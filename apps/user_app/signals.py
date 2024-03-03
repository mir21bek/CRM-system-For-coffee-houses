from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ClientProfile, CustomUser, EmployeeProfile


User = get_user_model()


@receiver(post_save, sender=CustomUser)
def create_client_profile(sender, instance, created, **kwargs):
    """Creates a profile when a new user is created"""
    print("Signal received for user:", instance)
    if created and hasattr(instance, "role") and instance.role == "client":
        print("Creating client profile for user:", instance)
        ClientProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def create_client_profile(sender, instance, created, **kwargs):
    """Creates a profile when a new user is created"""
    print("Signal received for user:", instance)
    if created:
        if hasattr(instance, "role") and (
            instance.role == "waiter"
            or instance.role == "barista"
            or instance.role == "admin"
        ):
            print("Creating client profile for user:", instance)
            EmployeeProfile.objects.create(user=instance)
        else:
            print("Not creating client profile for user:", instance)
