# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('receive_json/', views.receive_json, name='receive_json'),
    path('receive_classify_json/', views.receive_classify_json, name='receive_classify_json'),
]