from django.shortcuts import render , redirect
from django.http import HttpRequest , HttpResponse

# Create your views here.

def home_view(request:HttpRequest):

    return render(request, "main/home.html")


def not_found_view(request:HttpRequest):
   return render(request, "main/not_found.html" )


def not_authrize_view(request:HttpRequest):
   return render(request, "main/not_authrized.html" )
