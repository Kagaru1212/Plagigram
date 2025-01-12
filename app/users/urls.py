from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('subscribe/<str:username>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:username>/', views.unsubscribe, name='unsubscribe'),

]
