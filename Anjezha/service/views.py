from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from accounts.models import Department

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