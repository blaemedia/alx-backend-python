from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def chats(request):
    return HttpResponse("List of chats will be displayed here.")    