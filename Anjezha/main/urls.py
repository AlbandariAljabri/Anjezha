from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("" , views.home_view , name="home_view"),
    path("not_found/" , views.not_found_view , name= "not_found_view"),
    path("not_authrize/" , views.not_authrize_view , name= "not_authrize_view"),
]