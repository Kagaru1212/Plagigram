from django import forms
from django.forms.models import inlineformset_factory
from .models import Post, UploadImage, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'user', 'tags']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['image']


PostUploadImageFormSet = inlineformset_factory(Post, UploadImage, fields=('image',), extra=1, can_delete=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
