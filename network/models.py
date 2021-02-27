from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=280, default="CS50 Web Project 4 Network")
    following = models.ManyToManyField(User, blank=True, related_name="following")

    def __str__(self):
        return f"{self.username}"


# Automatically create Profile model when User after register a User
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)
        print('Profile created!')

#post_save.connect(create_profile, sender=User)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()
        print('Profile updated!')

#post_save.connect(update_profile, sender=User)