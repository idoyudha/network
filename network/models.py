from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.fields import related


class User(AbstractUser):
    pass

class Tweet(models.Model):
    user_tweet = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='user_liked', blank=True)

    def __str__(self):
        return f"{self.user_tweet}: {self.tweet_text[0:10]}"
