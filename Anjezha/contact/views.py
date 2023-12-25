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

