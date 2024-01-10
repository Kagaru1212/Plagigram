from django import forms
from django.forms.models import inlineformset_factory
from .models import Post, UploadImage, Comment, TagPost


class AddPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'user' in self.fields:
            del self.fields['user']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = ['image']


PostUploadImageFormSet = inlineformset_factory(Post, UploadImage, fields=('image',), extra=1, can_delete=True)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
