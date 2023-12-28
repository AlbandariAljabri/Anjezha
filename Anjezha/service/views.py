from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from accounts.models import *
from .models import *

# Create your views here.


# is_supervisor = booleanfield(false)

def add_department(request: HttpRequest):
    if request.method == "POST":
        new_department = Department(
            title=request.POST["title"], description=request.POST["description"], image=request.FILES["image"])
        new_department.save()
        return redirect("service:display_department")
    return render(request, "service/add_department.html")


def display_department(request: HttpRequest):

    department = Department.objects.all()
    return render(request, "service/display_department.html", {"department": department})


def department_details(request: HttpRequest, department_id):

    department = Department.objects.get(id=department_id)
    available_supervisors = Profile.objects.exclude(user=department.supervisor)
    available_worker = Profile.objects.exclude(
        user__in=department.worker.all())

    return render(request, "service/department_details.html", {"department": department, 'available_supervisors': available_supervisors, 'available_worker': available_worker})


def update_department(request: HttpRequest, department_id):
    department = Department.objects.get(id=department_id)

    if request.method == "POST":
        department.title = request.POST["title"]
        department.description = request.POST["description"]
        department.image = request.FILES["image"]
        department.save()

        return redirect("service:display_department")
    return render(request, "service/update_department.html", {"department": department})


def delete_department(request: HttpRequest, department_id):

    department = Department.objects.get(id=department_id)
    department.delete()
    return redirect("service:display_department")


def add_department_worker(request: HttpRequest, department_id, worker_id):
    department = Department.objects.get(id=department_id)
    worker = Profile.objects.get(id=worker_id)
    department.workers.add(worker.user)

    return redirect("service:department_details", department_id=department_id)


def remove_department_worker(request: HttpRequest, department_id, worker_id):
    if not request.user.has_perm("worker.delete_worker"):
        return render(request, "main/not_authrized.html")

    department = Department.objects.get(id=department_id)
    worker = Profile.objects.get(id=worker_id)
    department.worker.remove(worker.user)

    return redirect("service:department_details", department_id=department_id)


def add_department_supervisor(request: HttpRequest, department_id, supervisor_id):
    department = Department.objects.get(id=department_id)
    supervisor = Profile.objects.get(id=supervisor_id)
    department.supervisor = supervisor.user
    department.save()

    return redirect("service:department_details", department_id=department_id)


def replace_department_supervisor(request, department_id, supervisor_id):
    department = Department.objects.get(id=department_id)
    new_supervisor = Profile.objects.get(id=supervisor_id)

    if department.supervisor:
        department.supervisor = None  # If there is a current supervisor, remove them

    department.supervisor = new_supervisor.user
    department.save()  # Set the new supervisor
    return redirect("service:department_details", department_id=department_id)


def display_task_view(request: HttpRequest, task_id):
    tasks = Task.objects.all()

    if request.method == "POST":
        new_comment = Comment(task=tasks, user=request.user,
                              content=request.POST["content"])
        if 'image' in request.FILES:
            new_comment.image = request.FILES["image"]
        new_comment.save()

    return render(request, "service/display_task.html", {"tasks": tasks})


def add_comment_view(request: HttpRequest, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        comment = Comment.objects.filter(task=task)
        comment_count = comment.count()

    return render(request, "service/display_task.html", {"tasks": task, "comment": comment, "comment_count": comment_count})


def add_task_view(request: HttpRequest):
    all_workers = User.objects.all()

    if request.method == 'POST':
        selected_worker_ids = request.POST.getlist('workers')

        task = Task(
            name=request.POST['name'],
            description=request.POST['description'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            address=request.POST['address'],
        )

        supervisor_id = request.user.id
        supervisor = User.objects.get(id=supervisor_id)
        task.supervisor = supervisor

        task.save()

        task.workers.set(selected_worker_ids)

        return redirect("service:display_task_view")

    return render(request, "service/add_task.html", {"all_workers": all_workers})


def delete_task_view(request: HttpRequest, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect("service:display_task_view")


def update_task_view(request: HttpRequest, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.start_date = request.POST['start_date']
        task.end_date = request.POST['end_date']
        task.address = request.POST['address']
        task.save()
        return redirect("service:display_task_view")
    return render(request, "service/update_task.html", {"task": task})
