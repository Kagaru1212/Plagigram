from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),  # http://localhost:8000/plagigram/
    path('addpost/', views.add_post, name='addpost'),  # http://localhost:8000/plagigram/addpost/
]
