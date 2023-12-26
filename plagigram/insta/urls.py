from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),  # http://localhost:8000/plagigram/
]
