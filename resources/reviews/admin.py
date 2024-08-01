from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.contrib.filters.admin import RangeNumericFilter
from memoize import memoize

from resources.reviews.models import Comment, Review


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('hash', 'customer', 'car', 'created_at', 'updated_at')
    search_fields = ('customer__user__username', 'car__model')
    readonly_fields = ('created_at', 'updated_at', 'hash')
    list_filter = (
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    autocomplete_fields = ('customer', 'car')
    fieldsets = (
        (None, {
            'fields': ('customer', 'car', 'content', 'hash')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @memoize(timeout=60 * 15)
    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('customer', 'car')
        return queryset


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('hash', 'customer', 'sale', 'rating', 'created_at', 'updated_at')
    list_filter = (
        ('rating', RangeNumericFilter),
        ('created_at', RangeDateTimeFilter),
        ('updated_at', RangeDateTimeFilter),
    )
    search_fields = ('customer__user__username', 'sale', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'hash')
    autocomplete_fields = ('customer', 'sale')
    fieldsets = (
        (None, {
            'fields': ('customer', 'sale', 'rating', 'comment', 'hash')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @memoize(timeout=60 * 15)
    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related('customer', 'sale')
        return queryset
