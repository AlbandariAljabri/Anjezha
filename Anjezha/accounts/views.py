from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login_view(request: HttpRequest):
    msg = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user:
            login(request, user)
            return redirect("main:home_view")
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