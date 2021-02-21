
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Profile page
    path("profile/<str:user_profile>", views.profile, name="profile"),

    # API Routes
    path("tweet", views.tweet, name="tweet"),
    path("tweet/<str:user>", views.tweet_all, name="tweet_all"),
]
