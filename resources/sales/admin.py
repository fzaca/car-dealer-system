import uuid

from django.contrib import admin
from django.utils.html import format_html
from memoize import memoize
from minio.error import S3Error
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter, RelatedDropdownFilter

from resources.constants import MINIO_BUCKET
from resources.sales.forms import InvoiceForm
from resources.sales.models import Sale, PaymentMethod, Payment, Invoice
from resources.utils.minio import get_minio_client, generate_public_url

minio_client = get_minio_client()


@admin.register(Sale)
class SaleAdmin(ModelAdmin):
    list_display = ('hash', 'car', 'brand', 'customer', 'created_at', 'updated_at')
    list_filter = (
        ('car__car_model__brand', RelatedDropdownFilter),
        ('customer', RelatedDropdownFilter),
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    search_fields = ('car__car_model__name', 'customer__user__username', 'customer__dni')
    readonly_fields = ('hash', 'created_at', 'updated_at')
    autocomplete_fields = ['car', 'customer']

    fieldsets = (
        ('Basic Information', {
            'fields': ('hash', 'car', 'customer')
        }),
        ('Additional Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @memoize(timeout=60 * 15)
    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            'car__car_model', 'car__car_model__brand', 'customer__user'
        )
        return queryset

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
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

    # Unfold
    compressed_fields = True


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('hash', 'sale_car', 'sale_brand', 'method', 'amount', 'date', 'created_at')
    list_filter = (
        ('date', RangeDateTimeFilter),
        ('method', RelatedDropdownFilter),
        ('created_at', RangeDateTimeFilter),
    )
    search_fields = ('sale__car__car_model__name', 'sale__customer__user__username', 'method__name')
    readonly_fields = ('date', 'hash')
    autocomplete_fields = ['sale', 'method']

    def sale_car(self, obj):  # noqa: PLR6301
        return obj.sale.car
    sale_car.short_description = 'Car'

    def sale_brand(self, obj):  # noqa: PLR6301
        return obj.sale.car.car_model.brand
    sale_brand.short_description = 'Brand'

    # Unfold
    compressed_fields = True


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    form = InvoiceForm
    list_display = ('hash', 'sale', 'sale_car', 'pdf_url', 'date', 'created_at', 'updated_at')
    list_filter = (
        ('date', RangeDateTimeFilter),
        ('sale', RelatedDropdownFilter),
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    search_fields = ('sale__car__car_model__name', 'sale__customer__user__username')
    readonly_fields = ('date', 'pdf_tag', 'hash')
    autocomplete_fields = ['sale']
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

    @memoize(timeout=60 * 15)
    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            'sale', 'sale__car', 'sale__car__car_model', 'sale__car__car_model__brand', 'sale__customer__user'
        )
        return queryset

    # Unfold
    compressed_fields = True
