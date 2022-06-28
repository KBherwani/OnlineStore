from django.contrib import admin

from account.models import User


class UserModelAdmin(admin.ModelAdmin):
    """Default Django UserModelAdmin"""

    readonly_fields = ("password",)
    list_display = [
        "email",
    ]


admin.site.register(User, UserModelAdmin)
