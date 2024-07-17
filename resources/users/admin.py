from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "is_staff",
                    "is_customer",
                    "is_salesperson",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
