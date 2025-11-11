from rest_framework import serializers
from .models import Chat, Message, User, Conversation, Attachment

class User(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class Attachment(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file_url', 'file_type', 'uploaded_at']

class Message(serializers.ModelSerializer):
    sender = User(read_only=True)
    attachments = Attachment(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'attachments']

class Conversation(serializers.ModelSerializer):
    participants = User(many=True, read_only=True)
    last_message = Message(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'last_message']

class Chat(serializers.ModelSerializer):
    conversation = Conversation(read_only=True)
    messages = Message(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'conversation', 'messages', 'started_at', 'ended_at']