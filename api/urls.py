# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('receive_json/', views.receive_json, name='receive_json'),
]