from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name="index"),

    # to be removed:
    # path("login", views.login, name="login"),
    # path("register", views.register, name="register"),

    path("calendar", views.calendar, name="calendar"),

    path("indiv_file_comment/<int:course_id>", views.indiv_file_comment, name="indiv_file_comment"),

    path("home", views.home, name="home"),
    path("todo", views.todo, name="todo"),
    path("todo/missing", views.todo_missing, name="todo_missing"),
    path("todo/done", views.todo_done, name="todo_done"),

    path("edit_profile", views.edit_profile, name="edit_profile"),

    # Instructor course indiv pages
    path("instruct/<int:course_id>", views.instruct_stream, name="instruct_stream"),
    path("instruct/people/<int:course_id>", views.instruct_people, name="instruct_people"),
    path("instruct/classwork/<int:course_id>", views.instruct_classwork, name="instruct_classwork"),
    path("instructor/mark/<int:course_id>", views.instruct_mark, name="instruct_mark"),

    # Student course indiv pages
    path("course/<int:course_id>", views.student_stream, name="student_stream"),
    path("course/people/<int:course_id>", views.student_people, name="student_people"),
    path("course/classwork/<int:course_id>", views.student_classwork, name="student_classwork"),
    path("submission/<int:course_id>/<int:task_id>", views.submission , name="submission"),

    # footer web pages
    path("about", views.about, name="about"),
    path("goals", views.goals, name="goals"),
    path("mission", views.mission, name="mission"),
    path("vision", views.vision, name="vision"),
    
    # API Routes
    path("user/<int:user_id>", views.user_api, name="user"),
    path("course/<int:course_id>", views.course_api, name="course"),
    path("instructor/mark/submission/<int:student_id>/<int:course_id>/<int:task_id>", views.submission_api, name="submission_api"),
    path("task/<int:student_id>", views.user_task, name="user_task"),

    # POST data 
    path("update/profile", views.update_profile, name="update_profile"),
    path("save/course", views.save_course, name="save_course"),
    path("join/course", views.join_course, name="join_course"),
    path("post/content/<int:course_id>", views.post_content, name="post_content"),
    path("save/attachment/<int:course_id>/<int:task_id>", views.save_attachment, name="save_attachment"),
    path("delete/attachment/<int:course_id>/<int:task_id>", views.del_attachment, name="del_attachment"),
    path("assign/hw_quiz/<int:course_id>", views.assign_task, name="assign_task"),
    path("assign/material/<int:course_id>", views.assign_material, name="assign_material"),
    path("remove/students/<int:course_id>", views.remove_students, name="remove_students"),
    path("grade/<int:student_id>/<int:course_id>/<int:task_id>", views.grade_act, name="grade_act"),
]

# for accessing uploaded profile picture
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)