from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats, name='chat_list'),
]