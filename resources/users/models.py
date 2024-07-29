from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.username}"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200)
    dni = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} ({self.dni})"


class Employee(models.Model):  # FIXME: Make this model more stable
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)  # FIXME: Create table for positions
    hire_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    department = models.CharField(max_length=100)  # FIXME: Create table for departments

    def __str__(self):
        return f"{self.user.username}"
