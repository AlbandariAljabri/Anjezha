from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError


# Create your views here.

# Login 
def login_view(request):
    msg = None
    if request.method == "POST":
    

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_superuser:
                login(request, user)
                return redirect("accounts:admin_home_view")
            elif user.is_staff:
                login(request, user)
                return redirect("service:display_task_view")
            else:
                login(request, user)
                return redirect("service:display_task_view")
        else:
            msg = "Please provide correct username and password"

    return render(request, "accounts/login.html", {"msg": msg})

# Logout
def logout_view(request: HttpRequest):

    if request.user.is_authenticated:
        logout(request)    

    return redirect("accounts:login_view")


def user_profile_view(request: HttpRequest ,user_id):

    try:
        user = User.objects.get(id=user_id)

    except:
        return render(request, 'main/not_found.html')
    return render(request, 'accounts/profile.html')

# Register
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


def update_user_view(request: HttpRequest):
    msg = None

    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                user : User = request.user
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                try:
                    profile : Profile = request.user.profile
                except Exception as e:
                    profile = Profile(user=user, birth_date=request.POST["birth_date"])
                    profile.save()

                profile.birth_date = request.POST["birth_date"]
                if 'avatar' in request.FILES: profile.avatar = request.FILES["avatar"]
                profile.save()
                return redirect("accounts:user_profile_view", user_id = request.user.id)

            else:
                return redirect("accounts:login_view")
        except IntegrityError as e:
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/update_profile.html", {"msg" : msg})

def admin_home_view (request:HttpRequest):
    return render(request, "accounts/admin_home.html")
