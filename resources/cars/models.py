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


class Trim(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    potential_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    fuel_type = models.CharField(max_length=50)
    engine_size = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name} ({self.year})"


class Car(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    trim = models.ForeignKey(Trim, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # NOTE: Final price
    image_url = models.URLField(max_length=200)
    color = models.CharField(max_length=50)
    registration_year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.car_model.name} {self.trim.name} ({self.year})"
