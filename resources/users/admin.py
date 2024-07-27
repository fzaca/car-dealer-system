from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin

from resources.users.forms import CustomUserChangeForm, CustomUserCreationForm
from resources.users.models import Customer, CustomUser, Employee


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'is_staff', 'is_customer', 'is_employee')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2", "email", "is_staff",
                "is_customer", "is_employee"
            ),
        }),
    )

    list_display = ('username', 'email', 'is_staff', 'is_customer', 'is_employee', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_customer', 'is_employee')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Unfold
    compressed_fields = True


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = ('user_id', 'phone', 'address', 'dni')
    search_fields = ('user_id__username', 'phone', 'address', 'dni')
    ordering = ('user_id',)

    # Unfold
    compressed_fields = True


@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ('user_id', 'position', 'hire_date', 'salary', 'department')
    search_fields = ('user_id__username', 'position', 'department')
    ordering = ('user_id',)

    # Unfold
    compressed_fields = True
