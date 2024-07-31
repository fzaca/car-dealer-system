import uuid

from django.contrib import admin
from django.utils.html import format_html
from minio.error import S3Error
from unfold.admin import ModelAdmin

from resources.constants import MINIO_BUCKET
from resources.sales.forms import InvoiceForm
from resources.sales.models import Sale, PaymentMethod, Payment, Invoice
from resources.utils.minio import get_minio_client, generate_public_url

minio_client = get_minio_client()


@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = ('hash', 'car', 'brand', 'customer', 'date')
    list_filter = ('date', 'car__car_model__brand', 'customer')
    search_fields = ('car__car_model__name', 'customer__user__username', 'customer__dni')
    readonly_fields = ('date', 'hash')

    def get_queryset(self, request):  # noqa: PLR6301
        queryset = super().get_queryset(request)
        return queryset.select_related('car__car_model', 'customer__user')

    def car_model(self, obj):  # noqa: PLR6301
        return obj.car.car_model.name
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
    search_fields = ('sale__car__car_model__name', 'sale__customer__user__username', 'method__name')
    readonly_fields = ('date',)

    def sale_car(self, obj):  # noqa: PLR6301
        return obj.sale.car
    sale_car.short_description = 'Car'

    # Unfold
    compressed_fields = True


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    form = InvoiceForm
    list_display = ('hash', 'sale_car', 'pdf_url', 'date')
    list_filter = ('date',)
    search_fields = ('sale__car__car_model__name', 'sale__customer__user__username')
    readonly_fields = ('date', 'pdf_tag', 'hash')
    fieldsets = (
        (None, {
            'fields': ('sale', 'date', 'pdf_file', 'pdf_tag')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('pdf_url', 'hash'),
        }),
    )

    def pdf_tag(self, obj):  # noqa: PLR6301
        return format_html(
            '<iframe src="{}" width="600" height="400" style="border: none;"></iframe>'.format(obj.pdf_url)
        )
    pdf_tag.short_description = 'Invoice PDF'

    def sale_car(self, obj):  # noqa: PLR6301
        return obj.sale.car
    sale_car.short_description = 'Car'

    def save_model(self, request, obj, form, change):
        pdf_file = form.cleaned_data.get('pdf_file')
        if pdf_file:
            self._handle_pdf_upload(request, obj, pdf_file)
        super().save_model(request, obj, form, change)

    def _handle_pdf_upload(self, request, obj, pdf_file):
        file_ext = pdf_file.content_type.split("/")[-1]
        file_name = f"invoices/{uuid.uuid4()}.{file_ext}"

        if obj.pk and obj.pdf_url:
            old_file_name = '/'.join(obj.pdf_url.split('/')[-2:])
            try:
                minio_client.remove_object(MINIO_BUCKET, old_file_name)
            except S3Error as e:
                self.message_user(request, f"Error deleting old invoice: {e}", level='error')

        try:
            minio_client.put_object(
                MINIO_BUCKET,
                file_name,
                pdf_file.file,
                length=pdf_file.size,
                content_type=pdf_file.content_type,
            )
            public_url = generate_public_url(file_name)
            obj.pdf_url = public_url
        except S3Error as e:
            self.message_user(request, f"Error uploading invoice: {e}", level='error')

    # Unfold
    compressed_fields = True
