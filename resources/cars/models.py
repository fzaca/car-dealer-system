from decimal import Decimal
from django.core.cache import cache
from django.db import models
from django.db.models import Max, Min, Q
from nanoid_field import NanoidField
from memoize import memoize


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

    @classmethod
    def get_all_cached(cls):
        cache_key = "brands"
        brands = cache.get(cache_key)
        if brands is None:
            brands = cls.objects.all()
            cache.set(cache_key, brands, timeout=300)  # Cache for 5 minutes
        return brands


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

    @classmethod
    def get_by_brand_cached(cls, brand_name):
        cache_key = f"car_models_{brand_name}"
        car_models = cache.get(cache_key)
        if car_models is None:
            if brand_name:
                car_models = cls.objects.filter(brand__name__icontains=brand_name)
            else:
                car_models = cls.objects.all()
            cache.set(cache_key, car_models, timeout=300)


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

    @classmethod
    def get_aggregates(cls):
        cache_key = "cars_aggregates"
        aggregates = cache.get(cache_key)
        if not aggregates:
            aggregates = cls.objects.aggregate(
                max_price=Max('price'),
                min_year=Min('year'),
                max_year=Max('year')
            )
            cache.set(cache_key, aggregates, timeout=300)
        return aggregates

    @classmethod
    def filter_cars(cls, filters):
        """Apply filters to the Car queryset."""
        cache_key = f"cars_{filters['brand']}_{filters['car_model']}_" \
                    f"{filters['body_type']}_{filters['min_price']}_" \
                    f"{filters['max_price']}_{filters['min_year']}_" \
                    f"{filters['max_year']}_{filters['items_per_page']}_{filters['page_number']}"

        cars = cache.get(cache_key)
        if cars is None:
            cars = cls.objects.select_related('car_model', 'car_model__brand', 'body_type')

            q_filters = Q(is_available=True)
            if filters['brand']:
                q_filters &= Q(car_model__brand__name__icontains=filters['brand'])
            if filters['car_model']:
                q_filters &= Q(car_model__name__icontains=filters['car_model'])
            if filters['body_type']:
                q_filters &= Q(body_type__name__icontains=filters['body_type'])
            if filters['min_price'] is not None:
                q_filters &= Q(price__gte=filters['min_price'])
            if filters['max_price'] is not None:
                q_filters &= Q(price__lte=filters['max_price'])
            if filters['min_year'] is not None:
                q_filters &= Q(year__gte=filters['min_year'])
            if filters['max_year'] is not None:
                q_filters &= Q(year__lte=filters['max_year'])

            cars = cars.filter(q_filters)
            cache.set(cache_key, cars, timeout=300)  # Cache for 5 minutes
        return cars

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
    def get_similar_cars(self, similarity_criteria=None):
        """Retrieve similar cars based on body type and year."""
        if similarity_criteria is None:
            similarity_criteria = {
                'year_range': 1,
                'body_type': True,
                'car_model': False,
                'price_range': Decimal('0.1')
            }

        q_filters = Q(is_available=True)

        if 'year_range' in similarity_criteria:
            year_range = similarity_criteria['year_range']
            q_filters &= Q(year__range=(self.year - year_range, self.year + year_range))

        if similarity_criteria.get('body_type'):
            q_filters &= Q(body_type=self.body_type)

        if similarity_criteria.get('car_model'):
            q_filters &= Q(car_model=self.car_model)

        if 'price_range' in similarity_criteria:
            price_range_percentage = similarity_criteria['price_range']
            price_min = self.price * (Decimal('1') - price_range_percentage)
            price_max = self.price * (Decimal('1') + price_range_percentage)
            q_filters &= Q(price__range=(price_min, price_max))

        similar_cars = Car.objects.filter(q_filters).exclude(id=self.id).select_related('car_model', 'body_type')[:5]

        return similar_cars


class FeaturedCar(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    featured_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car.car_model.name} ({self.car.year})"
