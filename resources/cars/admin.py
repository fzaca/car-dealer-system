from django.contrib import admin

from resources.cars.models import Brand, CarModel


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')
    ordering = ('name',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
