from django.contrib import admin
from .models import TagPost, Post

admin.site.register(Post)
admin.site.register(TagPost)
