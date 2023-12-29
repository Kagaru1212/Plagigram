from django.shortcuts import render, redirect

from insta.forms import AddPostForm, PostUploadImageFormSet
from insta.models import Post


def index(request):
    posts = Post.objects.all()
    data = {
        'title': 'Plagigram',
        'posts': posts,
    }
    return render(request, 'insta/index.html', context=data)


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
