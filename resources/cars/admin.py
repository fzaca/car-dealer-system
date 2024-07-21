from django.contrib import admin

from resources.cars.forms import CarForm, CarModelForm, TrimForm
from resources.cars.models import Brand, Car, CarModel, Trim


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    form = CarModelForm
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')
    ordering = ('name',)


@admin.register(Trim)
class TrimAdmin(admin.ModelAdmin):
    form = TrimForm
    list_display = ('name', 'car_model', 'year', 'potential_price', 'fuel_type', 'engine_size')
    search_fields = ('name', 'car_model__name', 'car_model__brand__name')
    ordering = ('car_model__brand__name', 'car_model__name', 'year')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    form = CarForm
    list_display = ('car_model', 'trim', 'year', 'price', 'color', 'registration_year', 'mileage')
    search_fields = ('car_model__name', 'trim__name', 'color')
    ordering = ('car_model__brand__name', 'car_model__name', 'trim__name', 'year')
