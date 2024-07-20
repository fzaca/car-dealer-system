from django.contrib import admin

from resources.cars.models import Brand, Car, CarModel, Trim


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')
    ordering = ('name',)


class TrimAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_model', 'year', 'potential_price', 'fuel_type', 'engine_size')
    search_fields = ('name', 'car_model__name', 'car_model__brand__name')
    ordering = ('car_model__brand__name', 'car_model__name', 'year')


class CarAdmin(admin.ModelAdmin):  # FIXME: Que muestre solo las versiones del car model seleccionado
    list_display = ('car_model', 'trim', 'year', 'price', 'color', 'registration_year', 'mileage')
    search_fields = ('car_model__name', 'trim__name', 'color')
    ordering = ('car_model__brand__name', 'car_model__name', 'trim__name', 'year')


admin.site.register(Brand, BrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Trim, TrimAdmin)
admin.site.register(Car, CarAdmin)
