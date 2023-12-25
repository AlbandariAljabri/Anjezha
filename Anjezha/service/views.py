from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import *
from contact.models import *
from accounts.models import *

# Create your views here.


def add_department(request: HttpRequest):
    if request.method == "POST":
        new_department = Department(title=request.POST["title"], description=request.POST["description"],
                         Image=request.FILES["Image"])
        new_department.save()
        return redirect("service:display_department")
    return render("service/add_department.html")

def display_department(request: HttpRequest):
    
    department = Department.objects.all()
    return render(request, "service/display_department.html", {"departments": department})

def department_details(request: HttpRequest, department_id):

    department_detail = Department.objects.get(id=department_id)
    return render(request,"service/department_details.html", {"department": department_detail})

def display_task_view(request : HttpRequest):
    tasks = Task.objects.all()
    print("Tasks:", tasks)  # Add this line for debug

    return render(request , "service/display_task.html" , {"tasks" : tasks})


def add_task_view(request : HttpRequest):
    if request.method == 'POST':
        task=Task(
        name = request.POST['name'],
        description = request.POST['description'],
        start_date = request.POST['start_date'],
        end_date = request.POST['end_date'],
        address = request.POST['address'],
        duration = request.POST['duration'],
        workers = request.POST.getlist('workers'),
        supervisor = request.user 
        )
        task.save()

        return redirect('service:display_task_view')  # Redirect to the task list page after adding a task

    # If it's a GET request, simply render the form
    return render(request, "service/add_task.html")

