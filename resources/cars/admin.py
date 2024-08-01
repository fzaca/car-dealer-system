import uuid

from django.core.cache import cache
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter, RelatedDropdownFilter
from minio.error import S3Error

from resources.cars.filters import GearboxDropdownFilter, FuelTypeDropdownFilter
from resources.cars.forms import CarForm, CarModelForm
from resources.cars.models import BodyType, Brand, Car, CarModel, FeaturedCar
from resources.constants import MINIO_BUCKET
from resources.utils.minio import get_minio_client, generate_public_url
from resources.utils.filters import GenericChoicesDropdownFilter, GenericRelatedDropdownFilter
from resources.utils.filters import GenericRangeNumericFilter, GenericSliderNumericFilter
from resources.utils.filters import GenericSingleNumericFilter


minio_client = get_minio_client()


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = (
        ('name', GenericChoicesDropdownFilter),
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )

    def get_queryset(self, request):
        queryset = cache.get('brand_queryset')
        if not queryset:
            queryset = super().get_queryset(request)
            cache.set('brand_queryset', queryset, timeout=60 * 15)
        return queryset

    # Unfold
    compressed_fields = True
    list_filter_submit = True


@admin.register(CarModel)
class CarModelAdmin(ModelAdmin):
    form = CarModelForm
    list_display = ('hash', 'name', 'brand', 'created_at', 'updated_at')
    readonly_fields = ('hash', 'created_at', 'updated_at')
    search_fields = ('name', 'brand__name')
    ordering = ('name',)
    autocomplete_fields = ('brand', )
    list_filter = (
        ('brand', GenericRelatedDropdownFilter),
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    fieldsets = (
        (None, {
            'fields': ('name', 'hash', 'brand')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        queryset = cache.get('carmodel_queryset')
        if not queryset:
            queryset = super().get_queryset(request).select_related('brand')
            cache.set('carmodel_queryset', queryset, timeout=60 * 15)
        return queryset

    # Unfold
    compressed_fields = True
    list_filter_submit = True


@admin.register(BodyType)
class BodyTypeAdmin(ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    list_filter = (
        ('name', GenericChoicesDropdownFilter),
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_queryset(self, request):
        queryset = cache.get('bodytype_queryset')
        if not queryset:
            queryset = super().get_queryset(request)
            cache.set('bodytype_queryset', queryset, timeout=60 * 15)
        return queryset

    # Unfold
    compressed_fields = True
    list_filter_submit = True


@admin.register(Car)
class CarAdmin(ModelAdmin):
    form = CarForm
    list_display = (
        'hash', 'car_model', 'year', 'price', 'color', 'mileage',
        'engine_size', 'gearbox', 'fuel_type', 'seats', 'doors',
        'body_type', 'is_available', 'car_image',
    )
    search_fields = (
        'car_model__name', 'car_model__brand__name', 'color',
        'gearbox', 'fuel_type', 'body_type__name'
    )
    list_filter = (
        'is_available',
        ('car_model__brand', RelatedDropdownFilter),
        ('year', GenericSliderNumericFilter),
        ('price', GenericRangeNumericFilter),
        ('mileage', GenericRangeNumericFilter),
        ('engine_size', GenericRangeNumericFilter),
        GearboxDropdownFilter,
        FuelTypeDropdownFilter,
        ('seats', GenericSingleNumericFilter),
        ('doors', GenericSingleNumericFilter),
        ('body_type', RelatedDropdownFilter),
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    ordering = ('car_model__brand__name', 'car_model__name', 'year')
    readonly_fields = ('image_tag', 'image_url', 'hash')
    autocomplete_fields = ['car_model', 'body_type']

    fieldsets = (
        ('Image', {
            'fields': ('image_tag', 'image_url', 'image_file'),
        }),
        ('Car Information', {
            'fields': (
                'hash', 'car_model', 'year', 'price',
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related(
            'car_model__brand', 'body_type'
        ).only(
            'hash', 'car_model__name', 'car_model__brand__name', 'year', 'price', 'color', 'mileage',
            'engine_size', 'gearbox', 'fuel_type', 'seats', 'doors', 'body_type__name', 'is_available', 'image_url'
        )
        return queryset

    def image_tag(self, obj):
        return format_html('<img src="{}" width="300" height="200" />'.format(obj.image_url))
    image_tag.short_description = 'Car Image'

    def car_image(self, obj):
        return format_html('<img src="{}" style="height: 50px;"/>', obj.image_url)
    car_image.short_description = 'Image'

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
            public_url = generate_public_url(file_name)
            obj.image_url = public_url
        except S3Error as e:
            self.message_user(request, f"Error uploading image: {e}", level='error')

    compressed_fields = True
    list_filter_submit = True
    list_fullwidth = False


@admin.register(FeaturedCar)
class FeaturedCarAdmin(ModelAdmin):
    list_display = ('car_image', 'car_hash', 'car', 'car_price', 'car_brand', 'featured_date')
    search_fields = ('car__car_model__name', 'car__year', 'car__car_model__brand__name')
    ordering = ('-featured_date',)
    list_filter = (
        ('car__car_model__brand', GenericRelatedDropdownFilter),
        ('car__price', GenericRangeNumericFilter),
        ('featured_date', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    readonly_fields = ('car_image', 'car_hash', 'car_price', 'car_brand', 'featured_date')
    autocomplete_fields = ('car', )

    fieldsets = (
        ('Car Information', {
            'fields': ('car_hash', 'car_price', 'car_brand', 'car_image')
        }),
        ('Featured Information', {
            'fields': ('featured_date',)
        }),
    )

    def get_queryset(self, request):
        cache_key = f'featuredcar_queryset_{request.user.id}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = super().get_queryset(request).select_related('car__car_model__brand')
            cache.set(cache_key, queryset, timeout=60 * 15)
        return queryset

    def car_brand(self, obj):  # noqa: PLR6301
        return obj.car.car_model.brand.name
    car_brand.short_description = 'Brand Name'

    def car_price(self, obj):  # noqa: PLR6301
        return obj.car.price
    car_price.short_description = 'Price'

    def car_hash(self, obj):  # noqa: PLR6301
        return obj.car.hash
    car_hash.short_description = 'Hash'

    def car_image(self, obj):  # noqa: PLR6301
        return format_html('<img src="{}" style="height: 50px;"/>', obj.car.image_url)
    car_image.short_description = 'Image'

    # Unfold
    compressed_fields = True
    list_filter_submit = True
