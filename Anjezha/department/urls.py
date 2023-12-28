from django.urls import path
from . import views

app_name = "department"

urlpatterns = [
    path("add/department/", views.add_department, name="add_department"),
    path("display/department/", views.display_department,
         name="display_department"),
    path("department/details/<department_id>/",
         views.department_details, name="department_details"),
    path("update/department/<department_id>/",
         views.update_department, name="update_department"),
    path("delete/department/<department_id>/",
         views.delete_department, name="delete_department"),
    path('add_department_worker/<department_id> <worker_id>',
         views.add_department_worker, name="add_department_worker"),
    path('add_department_supervisor/<department_id>/<supervisor_id>',
         views.add_department_supervisor, name="add_department_supervisor"),
    path('remove/<department_id>/<worker_id>',
         views.remove_department_worker, name="remove_department_worker"),
    path('replace_department_supervisor/<department_id>/<supervisor_id>/',
         views.replace_department_supervisor, name='replace_department_supervisor'),
]
