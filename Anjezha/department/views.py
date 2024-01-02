from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .models import *
from accounts.models import *


# Create your views here.

# is_supervisor = booleanfield(false)

def add_department(request: HttpRequest):
    if request.method == "POST":
        new_department = Department(title=request.POST["title"], description=request.POST["description"])
        if 'image' in request.FILES: new_department.image = request.FILES["image"]
        new_department.save()
        return redirect("department:display_department")
    return render(request, "department/add_department.html")


def display_department(request: HttpRequest):

    department = Department.objects.all()

    return render(request, "department/display_department.html", {"department": department})


def department_details(request: HttpRequest, department_id):
    msg = None
    try:
        department = Department.objects.get(id=department_id)
        workers = User.objects.filter(groups__name="workers")
        supervisors = User.objects.filter(groups__name="supervisors")
    except Exception as e:
        msg = {e}

    return render(request, "department/department_details.html", {"department": department, 'supervisors': supervisors, 'workers': workers, "msg": msg})


def update_department(request: HttpRequest, department_id):
    department = Department.objects.get(id=department_id)

    if request.method == "POST":
        department.title = request.POST["title"]
        department.description = request.POST["description"]
        department.image = request.FILES["image"]
        department.save()

        return redirect("department:display_department")
    return render(request, "department/update_department.html", {"department": department})


def delete_department(request: HttpRequest, department_id):

    department = Department.objects.get(id=department_id)
    department.delete()
    return redirect("department:display_department")


def add_department_worker(request: HttpRequest, department_id, worker_id):
    department = Department.objects.get(id=department_id)
    workers = User.objects.get(id=worker_id)
    department.worker.add(workers)

    return redirect("department:department_details", department_id=department_id)


def remove_department_worker(request: HttpRequest, department_id, worker_id):

    department = Department.objects.get(id=department_id)
    workers = User.objects.get(id=worker_id)
    department.worker.remove(workers)

    return redirect("department:department_details", department_id=department_id)


def add_department_supervisor(request: HttpRequest, department_id, supervisor_id):
    department = Department.objects.get(id=department_id)
    supervisor = User.objects.get(id=supervisor_id)
    department.supervisor = supervisor
    department.save()

    return redirect("department:department_details", department_id=department_id)

