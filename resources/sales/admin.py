from django.contrib import admin
from unfold.admin import ModelAdmin

from resources.sales.models import Sale, PaymentMethod, Payment, Invoice


@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = ('car', 'customer', 'date', 'car_availability')
    list_filter = ('date', 'car__car_model__brand', 'customer')
    search_fields = ('car__car_model__name', 'customer__user_id__username', 'customer__dni')
    readonly_fields = ('date',)

    def car_availability(self, obj):  # noqa: PLR6301
        return obj.car.is_available
    car_availability.boolean = True
    car_availability.short_description = 'Car Available'

    # Unfold
    compressed_fields = True


@admin.register(PaymentMethod)
class PaymentMethodAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    # Unfold
    compressed_fields = True


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('sale', 'method', 'amount', 'date')
    list_filter = ('date', 'method')
    search_fields = ('sale__car__car_model__name', 'sale__customer__user_id__username', 'method__name')
    readonly_fields = ('date',)

    # Unfold
    compressed_fields = True


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ('sale', 'pdf', 'date')
    list_filter = ('date',)
    search_fields = ('sale__car__car_model__name', 'sale__customer__user_id__username')
    readonly_fields = ('date',)

    # Unfold
    compressed_fields = True
