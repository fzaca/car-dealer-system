from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from resources.users.models import Customer, CustomUser, Employee


@receiver(post_save, sender=CustomUser)
def manage_customer(sender, instance, **kwargs):
    if instance.is_customer:
        Customer.objects.get_or_create(user_id=instance)
    else:
        Customer.objects.filter(user_id=instance).delete()


@receiver(post_save, sender=CustomUser)
def manage_employee(sender, instance, **kwargs):
    if instance.is_employee:
        Employee.objects.get_or_create(user_id=instance)
    else:
        Employee.objects.filter(user_id=instance).delete()


@receiver(post_delete, sender=Customer)
def update_user_on_customer_delete(sender, instance, **kwargs):
    user = instance.user_id
    user.is_customer = False
    user.save()


@receiver(post_delete, sender=Employee)
def update_user_on_employee_delete(sender, instance, **kwargs):
    user = instance.user_id
    user.is_employee = False
    user.save()
