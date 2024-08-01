from django.db import models
from nanoid_field import NanoidField
from memoize import memoize


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class CarModel(models.Model):
    hash = NanoidField(max_length=10, alphabet="1234567890ABCDEF", editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['name']


class BodyType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['name']


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car_model.name} ({self.year})"

    class Meta:
        indexes = [
            models.Index(fields=['car_model']),
            models.Index(fields=['body_type']),
            models.Index(fields=['price']),
            models.Index(fields=['year']),
            models.Index(fields=['is_available']),
            models.Index(fields=['created_at']),
        ]

    @memoize(timeout=60 * 15)
    def get_related_cars(self):
        return (
            Car.objects
            .filter(car_model=self.car_model, year=self.year)
            .select_related('car_model', 'body_type')
        )

    @memoize(timeout=60 * 15)
    def get_average_price_by_model(self):
        return (
            Car.objects
            .filter(car_model=self.car_model)
            .aggregate(models.Avg('price'))['price__avg']
        )

    @memoize(timeout=60 * 5)
    def get_similar_cars(self):
        return (
            Car.objects
            .filter(
                body_type=self.body_type,
                year__range=(self.year - 1, self.year + 1)
            )
            .select_related('car_model', 'body_type')
        )


class FeaturedCar(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    featured_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car.car_model.name} ({self.car.year})"
