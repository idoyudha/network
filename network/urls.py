
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
    path("unfollow/<str:user_profile>", views.unfollow, name="unfollow"), # unfollow user

    # Just tweets from following user
    path("following", views.tweet_following, name="following"),

    # API Routes
    path("tweet", views.tweet, name="tweet"), 
    path("tweet_id/<int:pk>", views.tweet_id, name="tweet_id"), # view all tweet json
    path("tweet/<str:user>", views.tweet_all, name="tweet_all"), # view tweet for specific user
    #path("edit_tweet", views.edit_tweet, name="edit_tweet") # edit tweet for specific id
]
