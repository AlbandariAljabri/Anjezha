from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User, Group
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from department.models import Department



# Create your views here.

# Login
def login_view(request):
    msg = None
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)


        if user:
            if not user.last_login:
                login(request, user)
                return redirect("accounts:reset_password_view")
            elif user.is_superuser:
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

# Profile
# def user_profile_view(request: HttpRequest, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#         profile = Profile.objects.get(user=user)
#         supervisor_department = profile.user.supervised_department  
#     except Exception as e:
#         return render(request, 'main/not_found.html')

#     return render(request, 'accounts/profile.html', {"supervisor_department": supervisor_department,"user": user })

def user_profile_view(request: HttpRequest, user_id):

    try:
        user = User.objects.get(id=user_id)
        department=Department.objects.all()

    except:
        return render(request, 'main/not_found.html')
    return render(request, 'accounts/profile.html', {"user": user ,"department":department})

# Register
def register_view (request):
    msg =None
    if request.method == "POST":
      try:
            user = User.objects.create_user(
                username=request.POST["username"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                password=request.POST["password"]
            )
            user.save()
            is_supervisor = request.POST.get("type") == "supervisor"

            if is_supervisor:
                user.groups.add(Group.objects.get_or_create(name="supervisors")[0])
            else:
                user.groups.add(Group.objects.get_or_create(name="workers")[0])


            # Sending email
            subject = f'{user.first_name} {user.last_name} , Information Profile . '
            message = f'Dear Mr.{user.first_name} {user.last_name},\nWelcome Aboard! We are happy to have you at anjezha :)\n\nPlease find your login details below:\n\nUsername: {user.username}\nPassword: {request.POST["password"]}\n\nFor any inquiries, please do not hesitate to contact our IT department at anjezhaa@gmail.com.\n\nWe look forward to working with you.\n\nBest regards,\n[Anjezha Team]'
            from_email = 'anjezhaa@gmail.com'
            to_email = user.email

            send_mail(subject, message, from_email, [to_email], fail_silently=False)
            return redirect("accounts:successfully_msg_view")

      except IntegrityError as e:
            msg = f"Please select another username"
      except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/register.html", {"msg": msg})

# Successfully msg
def successfully_msg_view(request: HttpRequest):

    return render(request, 'accounts/successfully_msg.html')

# Update
def update_user_view(request: HttpRequest):
    msg = None

    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                user: User = request.user
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                try:
                    profile: Profile = request.user.profile
                except Exception as e:
                    profile = Profile(
                        user=user, birth_date=request.POST["birth_date"])
                    profile.save()

                profile.birth_date = request.POST["birth_date"]
                if 'avatar' in request.FILES:
                    profile.avatar = request.FILES["avatar"]
                profile.save()
                return redirect("accounts:user_profile_view", user_id=request.user.id)

            else:
                return redirect("accounts:login_view")
        except IntegrityError as e:
            print(e)
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/update_profile.html", {"msg": msg})

# Home
def admin_home_view(request: HttpRequest):
    return render(request, "accounts/admin_home.html")

# reset password
def reset_password_view(request: HttpRequest):
    try:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)          
                messages.success(request, 'Your password was successfully updated!')
                return redirect('accounts:user_profile_view', user_id=request.user.id)
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = PasswordChangeForm(request.user)
    except :
        return render(request , "main/not_found.html")
    return render(request, "accounts/reset_password.html", {"form": form})


# view supervisor rating

#superviser write rating
def rate_worker_view(request:HttpRequest):
    msg = None
    msg1 = None

    workers = User.objects.filter(groups__name="workers")

    if request.method == 'POST':
        worker_username = request.POST.get('worker_username')
        rating_value = request.POST.get('supervisor_rating')

        if worker_username and rating_value:
            try:
                worker = User.objects.get(username=worker_username)
                worker_profile = worker.profile
                worker_profile.supervisor_rating = int(rating_value)
                worker_profile.save()
                msg1= "Rating is send"
                return render(request, 'accounts/rate_worker.html' , {"msg1" : msg1})
            except User.DoesNotExist:
                msg = f"Worker with username {worker_username} not found."
            except ValueError:
                msg = "Invalid rating value."

    return render(request, 'accounts/rate_worker.html', {"workers": workers, "msg": msg})

# view rating
def display_supervisor(request: HttpRequest):

    supervisors = User.objects.filter(groups__name="supervisors")
    return render(request, "accounts/display_supervisor.html", {"supervisors": supervisors})


def display_worker(request: HttpRequest):

    workers = User.objects.filter(groups__name="workers")
    return render(request, "accounts/display_worker.html", {"workers": workers})

#worker view his rating
def worker_rating_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return render(request, 'accounts/profile.html', {"user": user})
    except User.DoesNotExist:
        return redirect('main:not_found_view')
    

