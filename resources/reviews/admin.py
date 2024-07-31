from django.contrib import admin
from django.core.cache import cache
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateTimeFilter
from unfold.contrib.filters.admin import RangeNumericFilter

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
    fieldsets = (
        (None, {
            'fields': ('customer', 'car', 'content', 'hash')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        queryset = cache.get('comment_queryset')
        if not queryset:
            queryset = super().get_queryset(request).select_related('customer', 'car')
            cache.set('comment_queryset', queryset, timeout=60 * 15)  # Cache por 15 minutos
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
    fieldsets = (
        (None, {
            'fields': ('customer', 'sale', 'rating', 'comment', 'hash')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        queryset = cache.get('review_queryset')
        if not queryset:
            queryset = super().get_queryset(request).select_related('customer', 'sale')
            cache.set('review_queryset', queryset, timeout=60 * 15)  # Cache por 15 minutos
        return queryset
