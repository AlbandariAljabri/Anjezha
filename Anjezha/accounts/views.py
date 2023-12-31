from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User, Group
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


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
                return redirect("accounts:reset_password_view")
                   
        else:
            msg = "Please provide correct username and password"

    return render(request, "accounts/login.html", {"msg": msg})

# Logout
def logout_view(request: HttpRequest):

    if request.user.is_authenticated:
        logout(request)    

    return redirect("accounts:login_view")

# Profile
def user_profile_view(request: HttpRequest, user_id):

    try:
        user = User.objects.get(id=user_id)

    except:
        return render(request, 'main/not_found.html')
    return render(request, 'accounts/profile.html', {"user":user})

# Register
def register_view (request:HttpRequest):
    msg =None
    if request.method == "POST":
        try:
            #create a new user
            user = User.objects.create_user(username=request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=request.POST["password"])
            user.save()

            is_supervisor = True if request.POST["type"] == "supervisor" else False

            supervisor_group, created = Group.objects.get_or_create(name="supervisors")
            worker_group, created = Group.objects.get_or_create(name="workers")

            if is_supervisor:
                user.groups.add(supervisor_group)
            else:
                user.groups.add(worker_group)
            return redirect("accounts:successfully_msg_view")
        except IntegrityError as e:
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"
     
    return render(request, "accounts/register.html", {"msg" : msg})

# Successfully msg
def successfully_msg_view(request:HttpRequest):

 return render(request, 'accounts/successfully_msg.html')

# Update
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
            print(e)
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/update_profile.html", {"msg" : msg})

# Home
def admin_home_view (request:HttpRequest):
    return render(request, "accounts/admin_home.html")


# reset password
def reset_password_view(request: HttpRequest):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:user_profile_view')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/reset_password.html", {"form": form })



#view supervisor rating
def rate_worker_view(request):
    msg = None
    workers = User.objects.filter(groups__name="workers")

    if request.method == 'POST':
        worker_username = request.POST.get('worker_username')
        rating = request.POST.get('rating')

        if worker_username and rating:
            try:
                worker_profile = Profile.objects.get(user__username=worker_username)
                worker_profile.supervisor_rating = int(rating)
                worker_profile.save()
                return redirect('accounts:rate_worker_view')
            except Profile.DoesNotExist as e:
                print(f"Error: {e}")
                msg = f"Worker profile not found for username: {worker_username}"
            except ValueError as e:
                print(f"Error: {e}")
                msg = "Invalid rating value."

    return render(request, 'accounts/rate_worker.html', {"workers": workers, "msg": msg})

# view rating
def worker_rating_view(request: HttpRequest):
    try:
        profile = request.user.profile
        supervisor_rating = profile.supervisor_rating
        return render(request, 'accounts/worker_profile.html', {"supervisor_rating": supervisor_rating})
    except Exception as e:
        msg = f"Something went wrong: {e}"
        return render(request, 'main/not_found.html', {"msg": msg})