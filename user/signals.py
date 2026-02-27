from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeProfile, User, Recuiter, RecuiterProfile

user = settings.AUTH_USER_MODEL

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("created True")
        if instance.type == User.user_type.EMPLOYE:
            EmployeProfile.objects.create(employe=instance)
            
        if instance.type == User.user_type.RECUITER:
            recuiter = Recuiter.objects.create(user=instance)
            RecuiterProfile.objects.create(recuiter = recuiter)
