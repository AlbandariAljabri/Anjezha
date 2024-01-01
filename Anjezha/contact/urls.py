from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("contact/", views.contact_view, name="contact_view"),
    path("confirmation/", views.thank_you_view, name="thank_you_view"),
    path('message/',views.message_view,name='message_view'),
    path('display/<message_id>',views.display_message_view,name="display_message_view"),
    path('update/<message_id>',views.status_view,name="status_view"),




]