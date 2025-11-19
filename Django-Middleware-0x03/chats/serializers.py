from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):  # ✅ Changed to UserSerializer
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):  # ✅ Changed to MessageSerializer
    # CharField example
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    message_type = serializers.CharField(default='text', max_length=20, required=False)
    
    # SerializerMethodField examples
    formatted_time = serializers.SerializerMethodField()
    is_edited = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'conversation', 'message_body', 
                 'message_type', 'sent_at', 'formatted_time', 'is_edited']
        read_only_fields = ['message_id', 'sender', 'sent_at']

    def get_formatted_time(self, obj):
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S") if obj.sent_at else None

    def get_is_edited(self, obj):
        return False

    def validate_message_body(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Message body cannot be empty")
        if len(value) > 1000:
            raise serializers.ValidationError("Message is too long (max 1000 characters)")
        return value

class ConversationSerializer(serializers.ModelSerializer):  # ✅ Changed to ConversationSerializer
    # CharField example
    conversation_title = serializers.CharField(max_length=100, required=False)
    
    # SerializerMethodField examples
    participant_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    participant_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'conversation_title',
                 'participant_count', 'last_message', 'participant_names']
        read_only_fields = ['conversation_id', 'created_at']

    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'message_body': last_msg.message_body,
                'sender_name': f"{last_msg.sender.first_name} {last_msg.sender.last_name}",
                'sent_at': last_msg.sent_at
            }
        return None

    def get_participant_names(self, obj):
        return [f"{user.first_name} {user.last_name}" for user in obj.participants.all()]

    def validate_conversation_title(self, value):
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError("Title must be at least 2 characters long")
        return value

    def create(self, validated_data):
        # Handle conversation creation with participants
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)  # This refers to the MODEL
        conversation.participants.set(participants)
        return conversation