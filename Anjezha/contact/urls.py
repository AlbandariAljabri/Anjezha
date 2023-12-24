from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("contact/", views.contact_view, name="contact_view"),
    path("comment/", views.add_comment_view, name="add_comment_view"),

]