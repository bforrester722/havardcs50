from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("following", views.following, name="following"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("toggle_follow/<str:username>", views.toggle_follow, name="toggle_follow"),
    path("toggle_like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
