from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>", views.categories, name="categories"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path(
        "listing/<int:listing_id>/close",
        views.close,
        name="close",
    ),
    path(
        "listing/<int:listing_id>/watch",
        views.change_watchlist,
        name="change_watchlist",
    ),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
]
