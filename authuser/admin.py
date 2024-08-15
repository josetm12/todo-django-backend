# authuser/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "last_login",
        "date_joined",
    )
    list_filter = ("email", "is_staff", "is_active", "last_login", "date_joined")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    readonly_fields = ("last_login", "date_joined")
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
