from django.shortcuts import render, HttpResponse

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from itertools import chain
from operator import attrgetter
import json, datetime, string, random
from django.views.decorators.csrf import csrf_exempt

from allauth.socialaccount.models import SocialAccount
from .models import User, Course, Post, Task, Submission

import os, io
from supabase import create_client, Client
from storage3.utils import StorageException

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# GENERATE RANDOM CLASSCODE
def classcode_generator():
    size = 7
    string_code = string.ascii_uppercase + string.digits
    return ''.join(random.choice(string_code) for _ in range(size))

# GENERATE THE NEXT FOLLOWING 6 DAYS FOR CALENDAR
def date():
    # calendar in dashboard
    week_date = dict()

    current_date = datetime.date.today()
    week_date[current_date.strftime("%a")] = current_date.strftime("%d")
    for _ in range(6):
        current_date = current_date + datetime.timedelta(days=1)
        week_date[current_date.strftime("%a")] = current_date.strftime("%d")
    
    return week_date

def index(request):
    return render(request, 'main/index/index.html')

@login_required
def home(request):
    week_date = date()

    # Check user login if via google
    try:
        user = SocialAccount.objects.get(user=request.user)
        course_enrolled = user.user.enrolled.all()
        course_instruct = user.user.instruct_course.all()

        if user.user.profile_url:
            user_profile = user.user.profile_url

            return render(request, 'main/S_home/S_home.html', {
                "user": user.user,
                "user_profile": user_profile,
                "enrolled_course": course_enrolled,
                "instruct_course": course_instruct,
                "week_date": week_date,
            })
        else:
            if user.provider == "google":
                # Google profile picture
                user_profile = user.extra_data['picture']

                return render(request, 'main/S_home/S_home.html', {
                    "user": user.user,
                    "user_profile": user_profile,
                    "enrolled_course": course_enrolled,
                    "instruct_course": course_instruct,
                    "week_date": week_date,
                })
            else:
                return render(request, 'main/S_home/S_home.html', {
                    "user": user.user,
                    "enrolled_course": course_enrolled,
                    "instruct_course": course_instruct,
                    "week_date": week_date,
                })
    # Manual Login
    except:
        if request.user.profile_url:
            return render(request, 'main/S_home/S_home.html', {
                "user": request.user,
                "user_profile": request.user.profile_url,
                "enrolled_course": request.user.enrolled.all(),
                "instruct_course": request.user.instruct_course.all(),
                "week_date": week_date,
            })
        
        return render(request, 'main/S_home/S_home.html', {
                    "user": request.user,
                    "enrolled_course": request.user.enrolled.all(),
                    "instruct_course": request.user.instruct_course.all(),
                    "week_date": week_date,
                })

def calendar(request):
    year = datetime.date.today().year
    return render(request, 'main/S_calendar/S_calendar.html', {
        "user": request.user,
        "year": year,
    })

def about(request):
    return render(request, 'main/footer-pages/about.html')

def goals(request):
    return render(request, 'main/footer-pages/goals.html')

def mission(request):
    return render(request, 'main/footer-pages/mission.html')

def vision(request):
    return render(request, 'main/footer-pages/vision.html')

def todo(request):
    user = request.user
    courses = user.enrolled.all()
    all_task = []
    task_today = []
    task_week = []

    theday = datetime.date.today()
    weekday = theday.isoweekday()
    start = theday - datetime.timedelta(days=weekday)
    dates = [start + datetime.timedelta(days=d) for d in range(7)]

    for course in courses:
        for task in course.task.all():
            if task.type != "MATERIAL":
                all_task.append(task.title)

                if task.due_date_time.date() == datetime.date.today():
                    task_today.append(task.title)
                
                if task.due_date_time.date() in dates:
                    task_week.append(task.title)

    return render(request, 'main/S_todo/S_todo.html', {
        "user": user,
        "all_task": all_task,
        "task_today": task_today,
        "task_week": task_week
    })

def edit_profile(request):
    return render(request, 'main/edit_profile/edit_profile.html')

# API ROUTE
def user_api(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(user.serialize())

def course_api(request, course_id):
    if request.method == "GET":
        course = Course.objects.get(pk=course_id)
        return JsonResponse(course.serialize())

@csrf_exempt
def submission_api(request, student_id, course_id, task_id):
    try:
        submission = Submission.objects.get(student_name=student_id, course=course_id, task=task_id)
    except Submission.DoesNotExist:
        return JsonResponse({"error": "No submission yet."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        grade = data.get("grade", "")

        submission.student_grade = grade
        submission.save()

        return HttpResponse(status=204)

def user_task(request, student_id):
    if request.method == "GET":
        user = User.objects.get(pk=student_id)
        courses = user.enrolled.all()
        all_task = courses.first().task.exclude(type="MATERIAL")
        for i in range(1, len(courses)):
            all_task = all_task.union(courses[i].task.exclude(type="MATERIAL"))

        return JsonResponse({"user": user.username, 
                             "tasks": [{"course": task.course.name,
                                        "title": task.title, 
                                        "due_month": task.due_date_time.strftime("%B"),
                                        "due_date": task.due_date_time.strftime("%-d"),
                                        "due_year": task.due_date_time.strftime("%Y"),} 
                                        for task in all_task ]}, status=200)


# =======================================================================

# POST method for updating profile
def update_profile(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        user = User.objects.get(pk=request.user.id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        try: 
            profile_picture = request.FILES["profilePicture"]
            bytes_content = profile_picture.read()

            res = supabase.storage.from_("profile").get_public_url(f"{user}/profile-picture.jpeg")
            try:
                res = supabase.storage.from_("profile").update(file=bytes_content, path=f'./{user}/profile-picture.jpeg', file_options={'cache-control': '3600', 'upsert': 'true', 'content-type': 'image/jpeg'})
            except StorageException:
                res = supabase.storage.from_("profile").upload(file=bytes_content, path=f"./{user}/profile-picture.jpeg", file_options={'content-type': 'image/jpeg'})

            profile_url = supabase.storage.from_("profile").get_public_url(f"{user}/profile-picture.jpeg")
            user.profile_url = profile_url

            """
            APPLICABLE ONLY DURING DEVELOPMENT
            user.profile_picture = profile_picture 
            """
            
            user.save()
        except:
            user.save()

        return HttpResponseRedirect(reverse("home"))

# POST method for course
def save_course(request):
    if request.method == "POST":
        course_name = request.POST["class_name"]
        course_code = request.POST["course_code"]
        section = request.POST["section"]
        room = request.POST["room"] 

        classcode = classcode_generator()

        while Course.objects.filter(classcode=classcode):
            classcode = classcode_generator()
        
        new_course = Course(name=course_name, 
                        section=section, 
                        course_code=course_code, 
                        room=room, 
                        instructor=request.user,
                        classcode=classcode)
        new_course.save()

        return HttpResponseRedirect(reverse("home"))

def join_course(request):
    if request.method == "POST":
        classcode = request.POST["classcode"]

        try:
            join_course  = Course.objects.get(classcode=classcode)
            join_course.students.add(request.user)
            return HttpResponseRedirect(reverse("home"))
        except:
            week_date = date()

            # Check login user if via Google
            try:
                msg = "Invalid Classcode."
                user = SocialAccount.objects.get(user=request.user)
                course_enrolled = user.user.enrolled.all()
                course_instruct = user.user.instruct_course.all()

                if(user.user.profile_url):
                    user_profile = user.user.profile_url

                    return render(request, 'main/S_home/S_home.html', {
                        "user": user.user,
                        "user_profile": user_profile,
                        "enrolled_course": course_enrolled,
                        "instruct_course": course_instruct,
                        "week_date": week_date,
                        "msg": msg,
                    })
                else:
                    if user.provider == "google":
                        # google profile picture
                        user_profile = user.extra_data['picture']

                        return render(request, 'main/S_home/S_home.html', {
                            "user": user.user,
                            "user_profile": user_profile,
                            "enrolled_course": course_enrolled,
                            "instruct_course": course_instruct,
                            "week_date": week_date,
                            "msg": msg,
                        })
                    else:
                        return render(request, 'main/S_home/S_home.html', {
                            "user": user.user,
                            "enrolled_course": course_enrolled,
                            "instruct_course": course_instruct,
                            "week_date": week_date,
                            "msg": msg,
                        })
            # Manual Login
            except:
                if request.user.profile_url:
                    user_profile = request.user.profile_url

                    return render(request, 'main/S_home/S_home.html', {
                        "user": request.user,
                        "user_profile": user_profile,
                        "enrolled_course": request.user.enrolled.all(),
                        "instruct_course": request.user.instruct_course.all(),
                        "week_date": week_date,
                        "msg": msg,
                    })
                
                return render(request, 'main/S_home/S_home.html', {
                            "user": request.user,
                            "enrolled_course": request.user.enrolled.all(),
                            "instruct_course": request.user.instruct_course.all(),
                            "week_date": week_date,
                            "msg": msg,
                })
    
# POST method for announcements / course post
def post_content(request, course_id):
    if request.method == "POST":
        user = request.user
        course = Course.objects.get(pk=course_id)
        content = request.POST["course-post-content"]
        new_post = Post(creator=user, content=content, course=course)
        new_post.save()

        # ask if user the student or instructor
        if course in user.instruct_course.all():
            return HttpResponseRedirect(reverse("instruct_stream", args=(course_id, )))
        else:
            return HttpResponseRedirect(reverse("student_stream", args=(course_id, )))

# POST attach file
def save_attachment(request, course_id, task_id):
    if request.method == "POST":
        user = request.user
        course = Course.objects.get(pk=course_id)
        task = Task.objects.get(pk=task_id)
        submission_status = True

        attach_file = request.FILES["attach-file"]
        file_bytes = attach_file.read()

        res = supabase.storage.from_("submission").get_public_url(f"{task}/{user}")
        try:
            res = supabase.storage.from_("submission").update(file=file_bytes, path=f'./{task}/{user}', file_options={'cache-control': '3600', 'upsert': 'true', 'content-type': attach_file.content_type})
        except StorageException:
            res = supabase.storage.from_("submission").upload(file=file_bytes, path=f"./{task}/{user}", file_options={'content-type': attach_file.content_type})

        attachment_url = supabase.storage.from_('submission').get_public_url(f"{task}/{user}")
        submit_file = Submission(student_name=user, course=course, task=task, submission_status=submission_status, attached_url=attachment_url)
        submit_file.save()

        return HttpResponseRedirect(reverse("submission", args=(course_id, task_id)))

# POST unsubmit attach file
def del_attachment(request, course_id, task_id):
    if request.method == "POST":
        user = request.user
        course = Course.objects.get(pk=course_id)
        task = Task.objects.get(pk=task_id)
        submission = Submission.objects.get(student_name=user.id, course=course.id, task=task.id)
        submission.delete()
        res = supabase.storage.from_("submission").remove(f"{task}/{user}")

        return HttpResponseRedirect(reverse("submission", args=(course_id, task_id)))

# POST assign hw / quiz
def assign_task(request, course_id):
    if request.method == "POST":
        course = Course.objects.get(pk=course_id)

        type = request.POST["assign-type"]
        title = request.POST["assign-title"]
        instruction = request.POST["assign-instruction"]
        points = request.POST["assign-points"]

        due_date_time = request.POST["assign-due-date"] + ' ' + request.POST["assign-due-time"]
        due_date_time = datetime.datetime.strptime(due_date_time,  '%Y-%m-%d %H:%M')

        new_task = Task(type=type, title=title, instruction=instruction, score=points, due_date_time=due_date_time, course=course)
        new_task.save()

        return HttpResponseRedirect(reverse("instruct_classwork", args=(course_id, )))

# POST material
def assign_material(request, course_id):
    if request.method == "POST":
        title = request.POST["material-title"]
        instruction = request.POST["material-instruction"]
        course = Course.objects.get(pk=course_id)

        new_material = Task(type="MATERIAL", title=title, instruction=instruction, course=course)
        new_material.save()

        return HttpResponseRedirect(reverse("instruct_classwork", args=(course_id, )))

# POST remove students 
def remove_students(request, course_id):
    if request.method == "POST":
        course = Course.objects.get(pk=course_id)
        student_id = request.POST.getlist("students")

        for id in student_id:
            student = User.objects.get(pk=id)
            course.students.remove(student)
        
        return HttpResponseRedirect(reverse("instruct_people", args=(course_id, )))

# POST grade
def grade_act(request, course_id, student_id, task_id):
    if request.method == "POST":
        submission = Submission.objects.get(student_name=student_id, course=course_id, task=task_id)
        grade = request.POST["score"]
        submission.student_grade = grade
        submission.save()

        return HttpResponseRedirect(reverse("instruct_mark", args=(course_id, )))

# Instructor indiv course pages
def instruct_stream(request, course_id):
    course = Course.objects.get(pk=course_id)
    course_task = course.task.all()
    course_post = course.post.all()

    merge_post = sorted(list(chain(course_task, course_post)),
                        key=attrgetter("date_time"),
                        reverse=True)
    
    return render(request, 'main/I_course/I_course_stream.html', {
        "course": course,
        "user": request.user,
        "all_post": merge_post,
    })

def instruct_classwork(request, course_id):
    course = Course.objects.get(pk=course_id)
    task = course.task.all()
    category = Task.CATEGORY
    return render(request, 'main/I_course/I_course_classwork.html', {
        "course": course,
        "user": request.user,
        "task": task,
        "category": category,
    })

def instruct_people(request, course_id):
    course = Course.objects.get(pk=course_id)
    return render(request, 'main/I_course/I_course_people.html', {
        "course": course,
    })

def instruct_mark(request, course_id):
    course = Course.objects.get(pk=course_id)
    tasks = course.task.all()
    students = course.students.all()

    return render(request, 'main/I_course/I_course_marks.html', {
        "course": course,
    })


# =================================================================

# Student indiv course pages
def student_stream(request, course_id):
    course = Course.objects.get(pk=course_id)

    # in stream, post announcment and task
    course_task = course.task.all()
    course_post = course.post.all()

    # merge post content and task, arrange from latest to oldest
    merge_post = sorted(list(chain(course_task, course_post)),
                        key=attrgetter("date_time"),
                        reverse=True)

    return render(request, 'main/S_course/S_course_stream.html', {
        "course": course,
        "user": request.user,
        "all_post": merge_post,
    })

def student_people(request, course_id):
    course = Course.objects.get(pk=course_id)
    instructor = course.instructor
    students = course.students.all()
    return render(request, 'main/S_course/S_course_people.html', {
        "course": course,
        "instructor": instructor,
        "students": students,
    })

def student_classwork(request, course_id):
    course = Course.objects.get(pk=course_id)
    task = course.task.all()
    return render(request, 'main/S_course/S_course_classwork.html', {
        "course": course,
        "user": request.user,
        "task": task,
    })

def submission(request, course_id, task_id):
    course = Course.objects.get(pk=course_id)
    task = course.task.get(pk=task_id)

    try:
        submission = Submission.objects.get(student_name=request.user, task=task.id)
        return render(request, 'main/S_submission/S_submission.html', {
            "course": course,
            "user": request.user, 
            "task": task,
            "submission": submission,
        })
    except:
        return render(request, 'main/S_submission/S_submission.html', {
            "course": course,
            "user": request.user, 
            "task": task,
        })