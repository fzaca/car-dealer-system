from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from resources.cars.forms import CarForm, CarModelForm
from resources.cars.models import BodyType, Brand, Car, CarModel


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

    # Unfold
    compressed_fields = True


@admin.register(CarModel)
class CarModelAdmin(ModelAdmin):
    form = CarModelForm
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')
    ordering = ('name',)

    # Unfold
    compressed_fields = True


@admin.register(BodyType)
class BodyTypeAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

    # Unfold
    compressed_fields = True


@admin.register(Car)
class CarAdmin(ModelAdmin):
    form = CarForm
    list_display = ('car_model', 'year', 'price', 'color', 'mileage', 'engine_size', 'gearbox', 'fuel_type', 'seats', 'doors', 'body_type', 'is_available')
    search_fields = ('car_model__name', 'car_model__brand__name', 'color', 'gearbox', 'fuel_type', 'body_type__name')
    list_filter = ('is_available', 'car_model__brand')
    ordering = ('car_model__brand__name', 'car_model__name', 'year')
    readonly_fields = ('image_tag',)

    fieldsets = (
        ('Image', {
            'fields': ('image_tag', 'image_url'),
        }),
        ('Car Information', {
            'fields': ('car_model', 'year', 'price', 'mileage', 'is_available'),
        }),
        ('Technical Specifications', {
            'fields': ('engine_size', 'gearbox', 'fuel_type'),
        }),
        ('Physical Characteristics', {
            'fields': ('color', 'seats', 'doors', 'body_type'),
        }),
    )

    def image_tag(self, obj):  # noqa: PLR6301
        return format_html('<img src="{}" width="300" height="200" />'.format(obj.image_url))

    image_tag.short_description = 'Car Image'

    # Unfold
    compressed_fields = True
