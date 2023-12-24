from django.urls import path
from . import views

app_name = "service"

urlpatterns = [
    path("display/task/" , views.display_task_view , name="display_task_view"),
]
