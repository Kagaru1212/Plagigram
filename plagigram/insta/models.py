from django.contrib.auth import get_user_model
from django.db import models

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.tag


class UploadImage(models.Model):
    image = models.ImageField(upload_to='images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(blank=True)

    objects = models.Manager()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    objects = models.Manager()
