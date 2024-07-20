from django.contrib import admin

from resources.cars.models import Brand, CarModel, Trim


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')
    ordering = ('name',)


class TrimAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_model', 'year', 'price', 'fuel_type', 'engine_size')
    search_fields = ('name', 'car_model__name', 'car_model__brand__name')
    ordering = ('car_model__brand__name', 'car_model__name', 'year')


admin.site.register(Brand, BrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Trim, TrimAdmin)
