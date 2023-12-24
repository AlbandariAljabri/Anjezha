from asyncio import tasks
from django.shortcuts import render , redirect
from django.http import HttpRequest , HttpResponse
from .models import Contact
from service.models import Task , Comment


# Create your views here.


def contact_view (request :HttpRequest):     
 msg = None
 if request.method == "POST":

        try:
            new_msg= Contact(user=request.user, subject=request.POST["subject"], message=request.POST["message"], status=request.POST["status"] , file= request.FILES["file"] )
            new_msg.save()
            return redirect("main:home_view")
        
        except Exception as e:
            msg = f"Please fill in all fields and try again. {e}"

        return render(request, "contact/contact.html", {"status" : Contact.status_choices,  "msg" : msg})


def add_comment_view(request: HttpRequest, task_id):

    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "main/not_authorized.html", status=401)

        task = tasks.objects.get(id=task_id)
        new_comment = Comment(task=task, user=request.user, content=request.POST["content"], comment=request.POST["comment"])
        if 'image' in request.FILES: new_comment.image = request.FILES["image"]
        new_comment.save()
    
        return redirect("service:movie_detail_view", task_id=new_comment.id)