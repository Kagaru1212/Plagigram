from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),  # http://localhost:8000/plagigram/
    path('addpost/', views.add_post, name='addpost'),  # http://localhost:8000/plagigram/addpost/
    path('post/<int:post_id>/', views.post_comments, name='comments'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
]
