from asyncio import tasks
from django.shortcuts import render , redirect
from django.http import HttpRequest , HttpResponse
from .models import Contact



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



# def add_comment_view(request: HttpRequest, task_id):
#     task = Task.objects.get(id=task_id)

#     if request.method == "POST":
#         if not request.user.is_authenticated:
#             return render(request, "main/not_authorized.html", status=401)

#         new_comment = Comment(task=task, user=request.user, content=request.POST["content"])
#         if 'image' in request.FILES: new_comment.image = request.FILES["image"]
#         new_comment.save()
#         return redirect("contact:add_comment_view", task_id=task.id)
#     return render(request , "contact/comment.html" , task_id=task.id)
