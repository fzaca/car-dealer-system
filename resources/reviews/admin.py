from django.contrib import admin
from unfold.admin import ModelAdmin

from resources.reviews.models import Comment, Review


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('id', 'customer', 'car', 'created_at', 'updated_at')
    list_filter = ('car', 'created_at', 'updated_at')
    search_fields = ('customer__user', 'car__car_model__name', 'content', 'car')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('id', 'customer', 'sale', 'rating', 'created_at', 'updated_at')
    list_filter = ('sale', 'rating', 'created_at', 'updated_at')
    search_fields = ('customer__user__username', 'sale__car', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('customer', 'sale', 'rating', 'comment')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
