from django.urls import path
from . import views

app_name = "service"

urlpatterns = [
    path("add/department/", views.add_department, name="add_department"),
    path("display/department/", views.display_department, name="display_department"),
    path("department/details/<department_id>/", views.department_details, name="department_details"),
    path("update/department/<department_id>/", views.update_department, name="update_department"),
    path("delete/department/<department_id>/", views.delete_department, name="delete_department"),
    path("display/task/" , views.display_task_view , name="display_task_view"),
    path("comment/add/<task_id>/", views.add_comment_view, name="add_comment_view"),
    path("add/task/" , views.add_task_view , name="add_task_view"),
    path('add_department_worker/<department_id> <worker_id>', views.add_department_worker, name="add_department_worker"),
    path('add_department_supervisor/<department_id>/<supervisor_id>', views.add_department_supervisor, name="add_department_supervisor"),
    path('remove/<department_id>/<worker_id>', views.remove_department_worker, name="remove_department_worker"),
    path('replace_department_supervisor/<department_id>/<supervisor_id>/', views.replace_department_supervisor, name='replace_department_supervisor'),
    path("delete/task/<task_id>/" , views.delete_task_view , name="delete_task_view"),
    path("update/task/<task_id>" , views.update_task_view , name="update_task_view")
]
