from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from accounts.models import Department
from .models import Task , Comment

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



def add_comment_view(request: HttpRequest, task_id):

    if request.method == "POST":
        
        if not request.user.is_authenticated:
            return render(request, "main/not_authorized.html", status=401)

        task = Task.objects.get(id=task_id)
        new_comment = Comment(task=task, user=request.user, content=request.POST["content"])
        if 'image' in request.FILES: new_comment.image = request.FILES["image"]
        new_comment.save()
    
        return redirect("service:display_task_view", task_id=task.id)
    
