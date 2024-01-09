from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from insta.forms import UploadImageForm, AddPostForm, PostUploadImageFormSet, CommentForm
from insta.models import UploadImage, Post, Comment
from plagigram import settings


@login_required
def index(request):
    posts = Post.objects.all()
    data = {
        'title': 'Plagigram',
        'posts': posts,
    }
    return render(request, 'insta/index.html', context=data)


@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = AddPostForm(request.POST)
        image_formset = PostUploadImageFormSet(request.POST, request.FILES, instance=Post())

        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save()
            image_formset.instance = post
            image_formset.save()

            return redirect('home')
    else:
        post_form = AddPostForm()
        image_formset = PostUploadImageFormSet(instance=Post())

    data = {
        'title': 'Add post',
        'form': post_form,
        'image_formset': image_formset
    }
    return render(request, 'insta/addpost.html', data)


@login_required
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    return render(request, 'insta/comments.html', {'post': post,
                                                   'comments': comments, 'form': form, 'title': 'Post',
                                                   'default_image': settings.DEFAULT_USER_IMAGE})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']
            if comment_text.strip():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()

    return redirect('comments', post_id=post_id)
