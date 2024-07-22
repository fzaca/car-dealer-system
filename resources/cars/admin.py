from django.contrib import admin
from unfold.admin import ModelAdmin

from resources.cars.forms import CarForm, CarModelForm
from resources.cars.models import Brand, Car, CarModel


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(CarModel)
class CarModelAdmin(ModelAdmin):
    form = CarModelForm
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')
    ordering = ('name',)


@admin.register(Car)
class CarAdmin(ModelAdmin):
    form = CarForm
    list_display = ('car_model', 'year', 'price', 'color', 'registration_year', 'mileage')
    search_fields = ('car_model__name', 'color')
    ordering = ('car_model__brand__name', 'car_model__name', 'year')
