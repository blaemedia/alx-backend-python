# chats/filters.py
import django_filters
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['conversation', 'sender']  # REMOVED 'timestamp'

class ConversationFilter(django_filters.FilterSet):
    class Meta:
        model = Conversation
        fields = ['participants']  # ONLY use fields that exist in your model