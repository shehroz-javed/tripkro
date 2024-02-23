from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (
            ("Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (("Personal info"), {"fields": ("username", "first_name", "last_name")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ]
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
