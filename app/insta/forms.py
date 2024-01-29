from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from .models import Post, UploadImage, Comment, TagPost
from cloudinary.forms import CloudinaryFileField


class AddPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['title', 'text', 'tags']


class UploadImageForm(forms.ModelForm):
    image = CloudinaryFileField()
    video_file = CloudinaryFileField(
        options={
            'folder': 'uploads',
            'resource_type': 'video',
            'allowed_formats': ['mp4', 'mov', 'avi'],
        }
    )

    class Meta:
        model = UploadImage
        fields = ['image', 'video_file']


PostUploadMediaFormSet = modelformset_factory(
    UploadImage,
    form=UploadImageForm,
    fields=('image', 'video_file'),
    extra=1,
    can_delete=True,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
