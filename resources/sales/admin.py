from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from resources.sales.models import Sale, PaymentMethod, Payment, Invoice


@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = ('car', 'brand', 'customer', 'date')
    list_filter = ('date', 'car__car_model__brand', 'customer')
    search_fields = ('car__car_model__name', 'customer__user_id__username', 'customer__dni')
    readonly_fields = ('date',)

    def car_model(self, obj):  # noqa: PLR6301
        return obj.car.car_model
    car_model.short_description = 'Car Model'

    def brand(self, obj):  # noqa: PLR6301
        return obj.car.car_model.brand
    brand.short_description = 'Brand'

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
    list_display = ('sale_car', 'method', 'amount', 'date')
    list_filter = ('date', 'method')
    search_fields = ('sale__car__car_model__name', 'sale__customer__user_id__username', 'method__name')
    readonly_fields = ('date',)

    def sale_car(self, obj):  # noqa: PLR6301
        return obj.sale.car
    sale_car.short_description = 'Car'

    # Unfold
    compressed_fields = True


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ('sale_car', 'pdf_url', 'date')
    list_filter = ('date',)
    search_fields = ('sale__car__car_model__name', 'sale__customer__user_id__username')
    readonly_fields = ('date', 'pdf_tag')

    def pdf_tag(self, obj):  # noqa: PLR6301
        return format_html(
            '<iframe src="{}" width="600" height="400" style="border: none;"></iframe>'.format(obj.pdf)
        )
    pdf_tag.short_description = 'Invoice PDF'

    def sale_car(self, obj):  # noqa: PLR6301
        return obj.sale.car
    sale_car.short_description = 'Car'

    # Unfold
    compressed_fields = True
