from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .models import *
from accounts.models import *


# Create your views here.

# is_supervisor = booleanfield(false)

def add_department(request: HttpRequest):
    if request.method == "POST":
        new_department = Department(title=request.POST["title"], description=request.POST["description"],image=request.FILES["image"])
        new_department.save()
        return redirect("service:display_department")
    return render(request, "service/add_department.html")


def display_department(request: HttpRequest):

    department = Department.objects.all()
    workers = User.objects.filter(groups__name="workers")
    supervisors = User.objects.filter(groups__name="supervisors")

    return render(request, "service/display_department.html", {"department": department ,'supervisors' : supervisors})


def department_details(request: HttpRequest, department_id):

    department = Department.objects.get(id=department_id)
    available_supervisors = Profile.objects.exclude(user=department.supervisor)
    available_worker = Profile.objects.exclude(user__in=department.worker.all())



    return render(request, "service/department_details.html", {"department": department, 'available_supervisors': available_supervisors, 'available_worker': available_worker,})


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
    department.worker.add(worker.user)

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
        department.supervisor = None  #If there is a current supervisor, remove them

    department.supervisor = new_supervisor.user
    department.save() #Set the new supervisor
    return redirect("service:department_details", department_id=department_id)

