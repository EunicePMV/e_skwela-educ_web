from django.db import models

from django.contrib.auth.models import AbstractUser
import os

"""
Custom User Model
"""
class User(AbstractUser):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    # profile_picture = models.ImageField(upload_to="users/", null=True, blank=True)
    profile_url = models.URLField(null=True, blank=True)
    
    def serialize(self):
        return {
            "user_id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "profile_url": self.profile_url,
        }
    
    # def filename(self):
    #     return os.path.basename(self.profile_picture.name)

class Course(models.Model):
    name = models.CharField(max_length=64)
    section = models.CharField(max_length=64, blank=True)
    course_code = models.CharField(max_length=64, null=True, blank=True)
    room = models.CharField(max_length=64, blank=True)
    banner = models.ImageField(upload_to="course/", blank=True) # if none then use the default course image 
    classcode = models.CharField(max_length=10, null=True)
    instructor = models.ForeignKey(User, related_name="instruct_course", on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name="enrolled", blank=True)

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "name": self.name,
            "section": self.section,
            "course_code": self.course_code,
            "room": self.room,
            "classcode": self.classcode,
            "instructor": self.instructor.username,
            "students": [student.username for student in self.students.all()],
            "all_post": [{
                "creator": post.creator.username, 
                "title":post.title, 
                "content": post.content, 
                "date_time": post.date_time.strftime("%b %d %Y")
            } for post in self.post.order_by("-date_time").all()],
            "all_task": [{
                "type": task.type,
                "title": task.title, 
                "instruction": task.instruction, 
                "score": task.score, 
                "due_date": task.due_date_time.strftime("%b %d %Y"),
                "due_time": task.due_date_time.strftime("%I:%M %p")
            } for task in self.task.all()]
        }

class Post(models.Model):
    creator = models.ForeignKey(User, related_name="post", null=True, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    date_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    course = models.ForeignKey(Course, related_name="post", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.creator}, {self.content}"

class Task(models.Model):
    CATEGORY = [
        ('ASSIGNMENT', 'Assignment'),
        ('QUIZ', 'Quiz'),
        ('MATERIAL', 'Material'),
    ]

    type = models.CharField(max_length=20, choices=CATEGORY)
    title = models.CharField(max_length=64)
    instruction = models.TextField()
    score = models.FloatField(null=True, blank=True)
    due_date_time = models.DateTimeField(null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    course = models.ForeignKey(Course, related_name="task", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Submission(models.Model):
    student_name = models.ForeignKey(User, related_name="submission", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="submission", on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name="submission", on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True, editable=False)
    submission_status = models.BooleanField(default=False)
    # attached_file = models.FileField(upload_to=f"submission/{course.name}", blank=True) APPLICABLE DURING DEVELOPMENT ONLY
    attached_url = models.URLField(blank=True, null=True)
    student_grade = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_name.username}"
    
    def filename(self):
        # return os.path.basename(self.attached_file.name) APPLICABLE DURING DEVELOPMENT ONLY
        return self.attached_url
    
    def serialize(self):
        return {
            "student_name": self.student_name.username,
            "course": self.course.name,
            "task": self.task.title,
            "student_grade": self.student_grade,
        }
