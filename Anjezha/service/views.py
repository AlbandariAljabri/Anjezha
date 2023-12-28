from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from accounts.models import *
from .models import *

# Create your views here.

# is_supervisor = booleanfield(false)



def display_task_view(request: HttpRequest ):
    tasks = Task.objects.all()

    
    return render(request, "service/display_task.html", {"tasks": tasks })


# def add_comment_view(request: HttpRequest, task_id):
#     task = Task.objects.get(id=task_id)

#     if request.method == "POST":

#         comment = Comment.objects.filter(task=task)
#         comment_count = comment.count()

#     return render(request, "service/display_task.html", {"task": task , "comment":comment , "comment_count":comment_count })






def add_task_view(request : HttpRequest):
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

    return render(request, "service/add_task.html" , {"all_workers" : all_workers })




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
        task.save()
        return redirect("service:display_task_view")
    return render(request, "service/update_task.html", {"task":task})
