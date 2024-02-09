from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm
from users.models import User, Subscription


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {"title": "Авторизация"}

    def form_valid(self, form):
        # Используйте кастомный бэкенд для аутентификации по email
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request=self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            # Обработайте случай, когда аутентификация не удалась
            return self.form_invalid(form)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
    }

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(get_user_model(), username=username)
    is_owner = request.user == profile_user

    is_following = Subscription.objects.filter(follower=request.user, followee=profile_user).exists()

    num_followers = profile_user.subscribers.count()
    num_following = profile_user.subscriptions.count()

    context = {
        'profile_user': profile_user,
        'is_owner': is_owner,
        'is_following': is_following,
        'num_followers': num_followers,
        'num_following': num_following,
        'title': "Профиль пользователя",
    }

    return render(request, 'users/user_profile.html', context)


@login_required
def subscribe(request, username):
    user_to_subscribe = get_object_or_404(User, username=username)

    # Проверяем, существует ли уже подписка
    if not Subscription.objects.filter(follower=request.user, followee=user_to_subscribe).exists():
        Subscription.objects.create(follower=request.user, followee=user_to_subscribe)

    return redirect('users:user_profile', username=username)


@login_required
def unsubscribe(request, username):
    user_to_unsubscribe = get_object_or_404(User, username=username)

    # Проверяем, существует ли подписка перед удалением
    subscription = Subscription.objects.filter(follower=request.user, followee=user_to_unsubscribe).first()
    if subscription:
        subscription.delete()

    return redirect('users:user_profile', username=username)

