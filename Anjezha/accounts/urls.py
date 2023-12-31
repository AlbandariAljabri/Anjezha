from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("profile/<user_id>/", views.user_profile_view, name="user_profile_view"),
    path("register/", views.register_view, name="register_view"),
    path("update/", views.update_user_view, name="update_user_view"),
    path("AdminHome/", views.admin_home_view, name="admin_home_view"),
    path('successfully/', views.successfully_msg_view, name='successfully_msg_view'),
    path('reset/password/', views.reset_password_view, name='reset_password_view'),
    path('rate/worker/', views.rate_worker_view, name='rate_worker_view'),
    path('rate/profile/<user_id>', views.worker_rating_view, name='worker_rating_view'),






]