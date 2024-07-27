from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.name}"


class BodyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Car(models.Model):
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

    def __str__(self):
        return f"{self.car_model.name} ({self.year})"
