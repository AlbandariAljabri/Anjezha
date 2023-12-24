from django.shortcuts import render , redirect
from django.http import HttpRequest , HttpResponse

# Create your views here.



def display_task_view(request : HttpRequest):
    return render(request , "service/display_task.html")