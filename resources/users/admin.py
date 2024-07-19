from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from resources.users.forms import CustomUserChangeForm, CustomUserCreationForm
from resources.users.models import Customer, CustomUser, Employee


class CustomUserAdmin(UserAdmin):
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


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone', 'address')
    search_fields = ('user_id__username', 'phone', 'address')
    ordering = ('user_id',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'position', 'hire_date', 'salary', 'department')
    search_fields = ('user_id__username', 'position', 'department')
    ordering = ('user_id',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee)
