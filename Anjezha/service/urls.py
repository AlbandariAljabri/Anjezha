from django.urls import path
from . import views

app_name = "service"

urlpatterns = [
   
   
    path("display/task/" , views.display_task_view , name="display_task_view"),
    path("comment/add/<task_id>/", views.add_comment_view, name="add_comment_view"),
    path("delete/task/<task_id>/" , views.delete_task_view , name="delete_task_view"),
    path("update/task/<task_id>" , views.update_task_view , name="update_task_view"),
    path('comment/reply/<comment_id>', views.add_reply_view, name="add_reply_view"),

    path("add/task/" , views.add_task_view , name="add_task_view"),
    path("mark_task_completed/<task_id>" , views.mark_task_completed , name="mark_task_completed"),

]
