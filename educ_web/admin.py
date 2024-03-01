from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Task, Course, Submission

class UserAdmin(UserAdmin):
    list_display = ["date_joined", "username", "email", "first_name", "last_name"]
    model = UserAdmin

    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Fields",
            {
                "fields": (
                    "profile_picture",
                )
            },
        ),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Task)
admin.site.register(Submission)
