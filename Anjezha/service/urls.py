from django.urls import path
from . import views

app_name = "service"

urlpatterns = [
    path("add/department", views.add_department, name="add_department"),
    path("display/department", views.display_department, name="display_department"),
    path("department/details/<department_id>/",
         views.department_details, name="department_details"),
    path("display/task/", views.display_task_view, name="display_task_view"),
]
