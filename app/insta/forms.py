from django import forms
from django.forms.models import inlineformset_factory
from .models import Post, UploadImage, Comment, TagPost
from cloudinary.forms import CloudinaryFileField


class AddPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags']


class UploadImageForm(forms.ModelForm):
    image = CloudinaryFileField()

    class Meta:
        model = UploadImage
        fields = '__all__'


PostUploadImageFormSet = inlineformset_factory(Post, UploadImage, fields=('image',), extra=1, can_delete=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
