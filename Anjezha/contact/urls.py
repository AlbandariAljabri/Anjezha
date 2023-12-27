from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("contact/", views.contact_view, name="contact_view"),
    path("confirmtaion/", views.thank_you_view, name="thank_you_view"),

]