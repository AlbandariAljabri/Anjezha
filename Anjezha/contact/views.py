from asyncio import tasks
from django.shortcuts import render , redirect
from django.http import HttpRequest , HttpResponse
from .models import Contact



# Create your views here.


def contact_view (request :HttpRequest):     
    msg = None
    if request.method == "POST":

        try:
            new_msg= Contact(user=request.user, subject=request.POST["subject"], message=request.POST["message"], status='Unread')
            if "file" in request.FILES:  new_msg.file = request.FILES["file"]
            new_msg.save()
            return redirect("contact:thank_you_view")
        
        except Exception as e:
            msg = f"Please fill in all fields and try again. {e}"

    return render(request, "contact/contact.html", {"status" : Contact.status_choices,  "msg" : msg})


def thank_you_view(request:HttpRequest):
    return render(request , "contact/thank_you.html ")

