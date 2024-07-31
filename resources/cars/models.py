from django.db import models
from nanoid_field import NanoidField


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class CarModel(models.Model):
    hash = NanoidField(max_length=10, alphabet="1234567890ABCDEF", editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"


class BodyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Car(models.Model):
    hash = NanoidField(max_length=10, alphabet="1234567890ABCDEF", editable=False)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    engine_size = models.DecimalField(max_digits=10, decimal_places=1)
    image_url = models.URLField(max_length=200)
    gearbox = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    year = models.PositiveIntegerField()  # NOTE: Anio de registro
    mileage = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()
    doors = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.car_model.name} ({self.year})"


class FeaturedCar(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    featured_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car.car_model.name} ({self.car.year})"
