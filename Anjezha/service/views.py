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
    return render(request , "service/display_task.html")


def add_task_view(request: HttpRequest):
    if request.method == 'POST':
        # Form submission
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        address = request.POST.get('address')
        duration = request.POST.get('duration')
        workers = request.POST.getlist('workers')  # Assuming workers is a multi-select field

        # Assuming you want to set the supervisor as the currently logged-in user
        supervisor = request.user

        # Validate the form data (add more validation as needed)
        if not all([name, description, start_date, end_date, address, duration, workers]):
            return render(request, "service/add_task.html", {'error_message': "Invalid form data. Please fill in all required fields."})

        # Save the task to the database
        task = Task.objects.create(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            address=address,
            duration=duration,
            supervisor=supervisor
        )
        task.workers.set(workers)

        return redirect('task_list')  # Redirect to the task list page after adding a task

    # If it's a GET request, simply render the form
    return render(request, "service/add_task.html")

