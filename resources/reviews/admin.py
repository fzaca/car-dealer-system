from django.contrib import admin
from unfold.admin import ModelAdmin

from resources.reviews.models import Comment, Review


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('hash', 'customer', 'car', 'created_at', 'updated_at')
    list_filter = ('car', 'created_at', 'updated_at')
    search_fields = ('customer__user', 'car__car_model__name', 'content', 'car')
    readonly_fields = ('created_at', 'updated_at', 'hash')


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('hash', 'customer', 'sale', 'rating', 'created_at', 'updated_at')
    list_filter = ('sale', 'rating', 'created_at', 'updated_at')
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
