from django.contrib import admin

from resources.cars.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Brand)
