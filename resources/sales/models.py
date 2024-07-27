from django.db import models

from resources.cars.models import Car
from resources.users.models import Customer


class Sale(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.car.is_available = False
        self.car.save()


class PaymentMethod(models.Model):  # FIXME: Add commands for load data
    name = models.CharField(max_length=50)


class Payment(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    pdf = models.URLField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
