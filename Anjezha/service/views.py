from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from accounts.models import *
from .models import *

# Create your views here.







def display_task_view(request: HttpRequest ):
    supervisors = User.objects.filter(groups__name="supervisors")
    workers = User.objects.filter(groups__name="workers")


    is_worker = request.user.groups.filter(name='workers').exists()
    is_supervisor = request.user.groups.filter(name='supervisors').exists()

    sort_order = request.GET.get('sort_order', 'ascending')
    created_at_filter = request.GET.get('created_at', '')
    completion_filter = request.GET.get('completion', '')

    if request.user in supervisors:
        tasks = Task.objects.filter(supervisor=request.user)
    else:
        tasks = Task.objects.filter(workers=request.user)

    # Apply filters
    if created_at_filter:
        tasks = tasks.filter(created_at=created_at_filter)

    if request.user.groups.filter(name='supervisors').exists():
        if completion_filter == 'completed':
            tasks = tasks.filter(supervisor_status="completed")
        elif completion_filter == 'not_completed':
            tasks = tasks.filter(supervisor_status="uncompleted")


    if request.user.groups.filter(name='workers').exists():
        if completion_filter == 'in_progress':
            tasks = tasks.filter(worker_status="in_progress")
        elif completion_filter == 'none':
            tasks = tasks.filter(worker_status="none")

    # Apply sorting
    if sort_order == 'ascending':
        tasks = tasks.order_by('created_at')
    elif sort_order == 'descending':
        tasks = tasks.order_by('-created_at')

    return render(request, "service/display_task.html", {"tasks": tasks , "supervisors" : supervisors , "is_worker":is_worker ,"is_supervisor" :is_supervisor , "supervisors":supervisors , "workers":workers})


# def mark_task_completed(request, task_id):
#     # Check if the user is a supervisor
#     supervisors = User.objects.filter(groups__name="supervisors")

#     if request.user in supervisors:
#         task = Task.objects.get(pk=task_id)
#         if task.completed == False:
#             task.completed = True
#             task.save()
#         else:
#             task.completed = False
#             task.save()

    
#     return redirect("service:display_task_view")


def update_status(request:HttpRequest, task_id):

    try:
        task = Task.objects.get(pk=task_id)

        # Check if the user is a worker and the task is assigned to them
        if request.user.groups.filter(name='workers').exists() and request.user in task.workers.all():

            if task.worker_status == 'in_progress':
                task.worker_status = 'none'
            else:
                task.worker_status = 'in_progress'
            task.save()

        # Check if the user is a supervisor
        elif request.user.groups.filter(name='supervisors').exists():
            # Toggle between 'completed' and 'uncompleted'
            if task.supervisor_status == 'completed':
                task.supervisor_status = 'uncompleted'
            else:
                task.supervisor_status = 'completed'
            task.save()

    except Task.DoesNotExist:
        pass

    return redirect("service:display_task_view")





def add_comment_view(request: HttpRequest, task_id ):
    tasks = Task.objects.get(id=task_id)

    if request.method=="POST":
            new_comment = Comment(task=tasks ,user=request.user ,content=request.POST["content"] )
            if 'image' in request.FILES: new_comment.image = request.FILES["image"]
            new_comment.save()
            return redirect('service:add_comment_view', task_id=tasks.id)
    
    comments = Comment.objects.filter(task=tasks)
    comment_count = comments.count()


    return render(request, "service/comment.html", {"comments": comments, "comment_count": comment_count, "task": tasks })


def add_reply_view(request: HttpRequest,  comment_id ):

    parent_comment = Comment.objects.get(id=comment_id)

    if request.method=="POST":
            reply = Reply(comment=parent_comment ,user=request.user ,reply_content=request.POST["reply_content"] )
            if 'reply_image' in request.FILES: reply.reply_image = request.FILES["reply_image"]
            reply.save()
            return redirect ('service:add_comment_view' ,  task_id=parent_comment.task.id)

    replies = Reply.objects.filter(comment=parent_comment) 

    return render(request, "service/comment.html", {"replies":replies ,"task":parent_comment.task})




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
    all_workers = User.objects.all()

    if request.method == "POST":
        selected_worker_ids = request.POST.getlist('workers')

        task.name = request.POST['name']
        task.description = request.POST['description']
        task.start_date = request.POST['start_date']
        task.end_date = request.POST['end_date']
        task.address = request.POST['address']
        
        task.save()

        task.workers.set(selected_worker_ids)

        return redirect("service:display_task_view")
    return render(request, "service/update_task.html", {"task": task , "all_workers" : all_workers})
