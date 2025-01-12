from cloudinary.uploader import upload
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload_large

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags')

    objects = models.Manager()


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)

    objects = models.Manager()

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('posts_by_tag', args=[str(self.tag)])


class UploadImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True, blank=True)
    image = CloudinaryField('images')


class UploadVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True, blank=True)
    video_file = CloudinaryField(resource_type='video')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(blank=True)

    objects = models.Manager()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    objects = models.Manager()
