from django.db.models.signals import post_save
from django.dispatch import receiver

from resources.cars.models import Car, FeaturedCar


@receiver(post_save, sender=Car)
def update_featured_car(sender, instance, **kwargs):
    if instance.is_featured:
        FeaturedCar.objects.get_or_create(car=instance)
    else:
        FeaturedCar.objects.filter(car=instance).delete()
