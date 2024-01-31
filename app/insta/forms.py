from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from .models import Post, UploadImage, Comment, TagPost, UploadVideo
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


class UploadVideoForm(forms.ModelForm):
    video_file = CloudinaryFileField(
        options={
            'folder': 'uploads',
            'resource_type': 'video',
            'allowed_formats': ['mp4', 'mov', 'avi'],
        }
    )

    class Meta:
        model = UploadVideo
        fields = '__all__'


PostUploadImageFormSet = inlineformset_factory(Post, UploadImage, form=UploadImageForm,
                                               fields=('image',), extra=1, can_delete=True, )

PostUploadVideoFormSet = inlineformset_factory(Post, UploadVideo, form=UploadVideoForm,
                                               fields=('video_file',), extra=1, can_delete=True, )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
