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
    conversation = serializers.CharField(source='conversation.title', read_only=True)  # CharField example
    messages = serializers.SerializerMethodField()  # SerializerMethodField example
    chat_status = serializers.CharField(max_length=20, required=False)  # Another CharField example
    duration = serializers.SerializerMethodField()  # Another SerializerMethodField example
    
    class Meta:
        model = Chat
        fields = ['id', 'conversation', 'messages', 'started_at', 'ended_at', 'chat_status', 'duration']
        read_only_fields = ['started_at', 'ended_at']

    def get_messages(self, obj):
        """Custom method to serialize messages with additional data"""
        from .serializers import MessageSerializer  # Import here to avoid circular imports
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True, context=self.context).data

    def get_duration(self, obj):
        """Calculate chat duration"""
        if obj.started_at and obj.ended_at:
            duration = obj.ended_at - obj.started_at
            return str(duration)
        return "Ongoing"

    def validate(self, data):
        """Validation using ValidationError"""
        if data.get('ended_at') and data.get('started_at'):
            if data['ended_at'] <= data['started_at']:
                raise serializers.ValidationError("End time must be after start time")
        
        # Validate chat status
        chat_status = data.get('chat_status')
        if chat_status and chat_status not in ['active', 'ended', 'archived']:
            raise serializers.ValidationError("Invalid chat status")
        
        return data

    # Alternative field-level validation
    def validate_chat_status(self, value):
        if value and value not in ['active', 'ended', 'archived', 'pending']:
            raise serializers.ValidationError("Status must be: active, ended, archived, or pending")
        return value