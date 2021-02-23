
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # Profile page
    path("profile/<str:user_profile>", views.profile, name="profile"),
    path("follow/<str:user_profile>", views.following, name="following"), # follow user
    path("unfollow/<str:user_profile>", views.unfollow, name="unfollow"), # follow user

    # API Routes
    path("tweet", views.tweet, name="tweet"), # view all tweet json
    path("tweet/<str:user>", views.tweet_all, name="tweet_all"), # view tweet for specific user
    
]
