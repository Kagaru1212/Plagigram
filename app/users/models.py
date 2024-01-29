from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    biography = models.TextField(blank=True, verbose_name="Biography")
    followers = models.ManyToManyField('self', symmetrical=True)

    def __str__(self):
        return self.username


class Subscription(models.Model):
    follower = models.ForeignKey(User, related_name='subscribers', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)

    objects = models.Manager()
