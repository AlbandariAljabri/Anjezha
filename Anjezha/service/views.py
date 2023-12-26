from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from accounts.models import Department
from .models import Task,Comment

# Create your views here.


def add_department(request: HttpRequest):
    if request.method == "POST":
        new_department = Department(title=request.POST["title"], description=request.POST["description"],
                                    Image=request.FILES["Image"])
        new_department.save()
        return redirect("service:display_department")
    return render(request, "service/add_department.html")


def display_department(request: HttpRequest):

    department = Department.objects.all()
    return render(request, "service/display_department.html", {"department": department})


def department_details(request: HttpRequest, department_id):

    department_detail = Department.objects.get(id=department_id)
    task = Task.objects.all()

    return render(request, "service/department_details.html", {"department": department_detail, "task": task})


def update_department(request: HttpRequest, department_id):
    department = Department.objects.get(id=department_id)

    if request.method == "POST":
       department.title = request.POST["title"]
       department.description = request.POST["description"]
       department.image = request.FILES["image"]
       department.save()

       return redirect("service:display_department")
    return render(request, "service/update_department.html", {"department":department})


def delete_department(request: HttpRequest, department_id):

    department = Department.objects.get(id=department_id)
    department.delete()
    return redirect("service:display_department")


def add_department_task(request: HttpRequest, department_id, task_id):
    department = Department.objects.get(id=department_id)
    task = Task.objects.get(id=task_id)
    department.task.add(task)
    return redirect("service:department_details", department_id=department_id)


def add_department_worker(request: HttpRequest, department_id, worker_id):
    department = Department.objects.get(id=department_id)
    worker = Task.objects.get(id=worker_id)
    department.worker.add(worker)
    return redirect("service:department_details", department_id=department_id)


def add_department_supervisor(request: HttpRequest, department_id, supervisor_id):
    department = Department.objects.get(id=department_id)
    supervisor = Task.objects.get(id=supervisor_id)
    department.supervisor.add(supervisor)
    return redirect("service:department_details", department_id=department_id)


def display_task_view(request : HttpRequest):
    tasks = Task.objects.all()
    print("Tasks:", tasks)  # Add this line for debug

    return render(request , "service/display_task.html" , {"tasks" : tasks})


def add_comment_view(request: HttpRequest, task_id):
    task = Task.objects.get(id=task_id)
    
    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "main/not_authorized.html", status=401)

        new_comment = Comment(task=task, user=request.user, content=request.POST["content"])
        if 'image' in request.FILES: new_comment.image = request.FILES["image"]
        new_comment.save()
        return redirect("contact:add_comment_view", task_id=task.id)
    return render(request , "contact/comment.html" , task_id=task.id)
  
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

