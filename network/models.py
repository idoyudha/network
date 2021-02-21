from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.fields import related
from datetime import datetime


class User(AbstractUser):
    pass

class Tweet(models.Model):
    user_tweet = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=280)
    timestamp = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='user_liked', blank=True)

    def __str__(self):
        return f"{self.user_tweet}: {self.tweet_text[0:10]}"

class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=280, default="CS50 Web Project 4 Network")
    followers = models.ManyToManyField(User, blank=True, related_name="followed_by")

    def __str__(self):
        return f"{self.username}"

