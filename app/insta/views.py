from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from insta.forms import AddPostForm, CommentForm, PostUploadImageFormSet, PostUploadVideoFormSet
from insta.models import Post, Comment, Like, TagPost
from cloudinary.uploader import upload

import cloudinary
import cloudinary.uploader
import cloudinary.api


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
        image_formset = PostUploadImageFormSet(request.POST, request.FILES, prefix='image')
        video_formset = PostUploadVideoFormSet(request.POST, request.FILES, prefix='video_file')

        if post_form.is_valid() and image_formset.is_valid() and video_formset.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()

            post.tags.set(post_form.cleaned_data['tags'])

            image_formset.instance = post
            image_formset.save()

            video_formset.instance = post
            video_formset.save()

            for video_file_instance in post.uploadvideo_set.all():
                video_file_url = upload_to_cloudinary(video_file_instance.video_file.url)
                video_file_instance.video_file = video_file_url
                video_file_instance.save()

            return redirect('home')

    else:
        post_form = AddPostForm()
        image_formset = PostUploadImageFormSet(prefix='image')
        video_formset = PostUploadVideoFormSet(prefix='video_file')

    tag_list = TagPost.objects.all()

    data = {
        'title': 'Add post',
        'form': post_form,
        'video_formset': video_formset,
        'image_formset': image_formset,
        'tag_list': tag_list,
    }
    return render(request, 'insta/addpost.html', data)


def upload_to_cloudinary(file, is_file_path=False):
    if is_file_path:
        with open(file, 'rb') as video_file:
            res = cloudinary.uploader.upload_large(video_file, resource_type="video")
    else:
        res = cloudinary.uploader.upload_large(file, resource_type="video")

    return res['secure_url']


@login_required
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()

    return render(request, 'insta/comments.html', {'post': post,
                                                   'comments': comments, 'form': form, 'title': 'Post'})


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


@login_required
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = request.user

    existing_like = Like.objects.filter(user=user, post=post).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(user=user, post=post)

    return redirect('home')


def posts_by_tag(request, tag):
    tag = get_object_or_404(TagPost, tag=tag)
    posts = Post.objects.filter(tags=tag)

    return render(request, 'insta/index.html', {'tag': tag, 'posts': posts, 'title': f"Posts by {tag}"})
