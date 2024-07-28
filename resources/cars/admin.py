import uuid

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from minio.error import S3Error

from resources.cars.forms import CarForm, CarModelForm
from resources.cars.models import BodyType, Brand, Car, CarModel, FeaturedCar
from resources.constants import MINIO_BUCKET
from resources.constants import MINIO_PUBLIC_HOST, MINIO_PUBLIC_URL
from resources.utils.minio_utils import get_minio_client

minio_client = get_minio_client()


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
    readonly_fields = ('image_tag', 'image_url')

    fieldsets = (
        ('Image', {
            'fields': ('image_tag', 'image_url', 'image_file'),
        }),
        ('Car Information', {
            'fields': (
                'car_model', 'year', 'price',
                'mileage', 'is_featured', 'is_available'
            ),
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

    def save_model(self, request, obj, form, change):
        image_file = form.cleaned_data.get('image_file')
        if image_file:
            self._handle_image_upload(request, obj, image_file)
        super().save_model(request, obj, form, change)

    def _handle_image_upload(self, request, obj, image_file):
        file_ext = image_file.content_type.split("/")[-1]
        file_name = f"cars/{uuid.uuid4()}.{file_ext}"

        if obj.pk and obj.image_url:
            old_file_name = '/'.join(obj.image_url.split('/')[-2:])
            try:
                minio_client.remove_object(MINIO_BUCKET, old_file_name)
            except S3Error as e:
                self.message_user(request, f"Error deleting old image: {e}", level='error')

        try:
            minio_client.put_object(
                MINIO_BUCKET,
                file_name,
                image_file.file,
                length=image_file.size,
                content_type=image_file.content_type,
            )
            public_url = self._generate_public_url(file_name)
            obj.image_url = public_url
        except S3Error as e:
            self.message_user(request, f"Error uploading image: {e}", level='error')

    def _generate_public_url(self, file_name):  # noqa: PLR6301
        if settings.ENV == "local":
            return f"http://{MINIO_PUBLIC_URL}/{MINIO_BUCKET}/{file_name}"
        else:
            return f"{MINIO_PUBLIC_HOST}/{MINIO_BUCKET}/{file_name}"

    # Unfold
    compressed_fields = True


@admin.register(FeaturedCar)
class FeaturedCarAdmin(ModelAdmin):
    list_display = ('car', 'car_price', 'car_brand', 'featured_date')
    search_fields = ('car__car_model__name', 'car__year', 'car__car_model__brand__name')
    ordering = ('-featured_date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('car__car_model__brand')

    def car_brand(self, obj):  # noqa: PLR6301
        return obj.car.car_model.brand.name
    car_brand.short_description = 'Brand Name'

    def car_price(self, obj):  # noqa: PLR6301
        return obj.car.price
    car_price.short_description = 'Price'

    # Unfold
    compressed_fields = True
