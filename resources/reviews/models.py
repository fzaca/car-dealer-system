from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from resources.cars.models import Car
from resources.sales.models import Sale
from resources.users.models import Customer


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'sale'],
                name='unique_review_per_customer_and_sale'
            )
        ]

    def __str__(self):
        return f"{self.customer.user} - {self.car} - {self.rating}"


class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer.user} - {self.car}"
