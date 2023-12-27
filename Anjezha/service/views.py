from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from accounts.models import Department, Profile
from .models import Task, Comment

# Create your views here.



# is_supervisor = booleanfield(false)

def add_department(request: HttpRequest):
    if request.method == "POST":
        new_department = Department(title=request.POST["title"], description=request.POST["description"],
                                    image=request.FILES["image"])
        new_department.save()
        return redirect("service:display_department")
    return render(request, "service/add_department.html")


def display_department(request: HttpRequest):

    department = Department.objects.all()
    return render(request, "service/display_department.html", {"department": department})


def department_details(request: HttpRequest, department_id):

    department = Department.objects.get(id=department_id)
    available_supervisors = Profile.objects.exclude(user=department.supervisor)
    available_workers = Profile.objects.exclude(
        user__in=department.workers.all())

    return render(request, "service/department_details.html", {"department": department, 'available_supervisors': available_supervisors, 'available_workers': available_workers})


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
    department.workers.remove(worker.user)

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

def display_task_view(request: HttpRequest):
    tasks = Task.objects.all()

    return render(request, "service/display_task.html", {"tasks": tasks})


def add_comment_view(request: HttpRequest, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "main/not_authorized.html", status=401)

        new_comment = Comment(task=task, user=request.user,
                              content=request.POST["content"])
        if 'image' in request.FILES:
            new_comment.image = request.FILES["image"]
        new_comment.save()
        return redirect("contact:add_comment_view", task_id=task.id)
    return render(request, "contact/comment.html", task_id=task.id)


def add_task_view(request: HttpRequest):
    if request.method == 'POST':
        task = Task(
            name=request.POST['name'],
            description=request.POST['description'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            address=request.POST['address'],
            duration=request.POST['duration'],
            workers=request.POST.getlist('workers'),
            supervisor=request.user
        )

    return render(request , "contact/display_task.html" , task_id=task.id)
  
def add_task_view(request : HttpRequest):
    if request.method == 'POST':
        task=Task(name = request.POST['name'],description = request.POST['description'],start_date = request.POST['start_date'],end_date = request.POST['end_date'],address = request.POST['address'],duration = request.POST['duration'])
        task.save()
        return redirect("service:display_task_view")  

        # Redirect to the task list page after adding a task
        return redirect('service:display_task_view')

    # If it's a GET request, simply render the form
    return render(request, "service/add_task.html")
    return render(request, "service/add_task.html")


def delete_task_view(request : HttpRequest , task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect("service:display_task_view")

def update_task_view(request : HttpRequest , task_id):
    task = Task.objects.get(id=task_id)

    if request.method == "POST":
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.start_date = request.POST['start_date']
        task.end_date = request.POST['end_date']
        task.address = request.POST['address']
        task.duration = request.POST['duration']
        task.save()
        return redirect("service:display_task_view")
    return render(request, "service/update_task.html", {"task":task})
