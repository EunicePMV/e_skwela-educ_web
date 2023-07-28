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

# fix many to many fields 
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ("name", "section", "course_code", "room", "banner", "classcode", "instructor", "students")
#     list_filter = ("name", "section", "course_code", "room", "banner", "classcode", "instructor", "students")

#     def get_students(self, obj):
#         return "\r\n".join([s.username for s in obj.students.all()])

# class PostAdmin(admin.ModelAdmin):
#     list_display = ("creator", "content", "date_time", "course")
#     list_filter = ("creator","content", "date_time", "course")

# class TaskAdmin(admin.ModelAdmin):
#     list_display = ("type", "title", "instruction", "score", "due_date", "due_time", "course")    
#     list_filter = ("type", "title", "instruction", "score", "due_date", "due_time", "course")

# admin.site.register(User, UserAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Task, TaskAdmin)

# class DiagnosiAdmin(admin.ModelAdmin):
#     list_filter = ('diagnosis_desc', 'drugs_desc', 'procedure')
#     list_display = ('diagnosis_desc', 'drugs_desc')

#     def get_procedure(self, obj):
#         return "\r\n".join([p.procedure_desc for p in obj.procedure.all()])