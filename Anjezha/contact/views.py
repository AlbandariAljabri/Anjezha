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

def message_view(request:HttpRequest,):
    message = Contact.objects.all()

    return render(request, "contact/messages.html", {"message" :message})

def display_message_view(request:HttpRequest ,message_id):
    message = Contact.objects.get(id=message_id)
    
    return render(request, "contact/display_message.html", {"message" : message })

def status_view(request:HttpRequest,message_id):

    if not request.user.is_staff:
        return render(request, "main/not_authorized.html", status=401)
    
    message = Contact.objects.get(id=message_id)

    if request.method == "POST":

        message.status = request.POST["status"]
        message.save()
    
        return redirect('contact:display_message_view' ,message_id)
    
    return render(request, 'contact/update_status.html',{"message": message ,"status_choices":Contact.status_choices})

def thank_you_view(request:HttpRequest):
    return render(request , "contact/thank_you.html")

