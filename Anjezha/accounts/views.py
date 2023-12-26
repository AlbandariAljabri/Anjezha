from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError


# Create your views here.

def login_view(request: HttpRequest):
    msg = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user and request.user.is_superuser:
            return redirect("accounts:admin_home_view")

        elif user and request.user.is_staff:
            return redirect("service:display_task_view")
        
        elif user and request.user.is_authenticated:
            #if in group
            login(request, user)
            return redirect("service:display_task_view")

        else:
            msg = "Please provide correct username and password"

    return render(request, "accounts/login.html", {"msg" : msg})


def logout_view(request: HttpRequest):

    if request.user.is_authenticated:
        logout(request)    

    return redirect("accounts:login_view")


def user_profile_view(request: HttpRequest):

    # try:
    #     user = User.objects.get(id=user_id)

    # except:
    #     return render(request, 'main/not_found.html')
    return render(request, 'accounts/profile.html')


def register_view (request:HttpRequest):
    msg =None
    if request.method == "POST":
        try:
            #create a new user
            user = User.objects.create_user(username=request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=request.POST["password"])
            user.save()
            return redirect("accounts:login_view")
        except IntegrityError as e:
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"
     
    return render(request, "accounts/register.html", {"msg" : msg})


def admin_home_view (request:HttpRequest):
    return render(request, "accounts/admin_home.html")
