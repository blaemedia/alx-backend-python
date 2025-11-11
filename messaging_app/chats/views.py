from django.shortcuts import render
from django.http import HttpResponse
from .serializers import Conversation,Message
from rest_framework import viewsets


# Create your views here.
def chats(request):
    return HttpResponse("List of chats will be displayed here.")   

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = Conversation

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = Message