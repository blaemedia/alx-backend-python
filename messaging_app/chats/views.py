# chats/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer, ConversationDetailSerializer
from .auth import JWTAuth, MessageJWTAuth

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated here
    serializer_class = ConversationSerializer

    def get_queryset(self):
        # Users can only see conversations they're part of
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages for a specific conversation
        """
        conversation = self.get_object()
        
        # Check if user is a participant in the conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN  # Add HTTP_403_FORBIDDEN
            )
        
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Send a message to a conversation
        """
        conversation = self.get_object()
        
        # Check if user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    """
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated here
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Users can only see messages from conversations they're part of
        return Message.objects.filter(
            models.Q(sender=self.request.user) | 
            models.Q(conversation__participants=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')  # Add conversation_id
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            # Check if user is a participant
            if self.request.user not in conversation.participants.all():
                return Response(
                    {"detail": "You are not a participant in this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer.save(sender=self.request.user, conversation=conversation)
        else:
            serializer.save(sender=self.request.user)


class ConversationMessagesAPIView(APIView):
    """
    API view to get messages for a specific conversation
    """
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated here

    def get(self, request, conversation_id):  # Add conversation_id parameter
        """
        Get all messages for a specific conversation
        """
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Check if user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Use Message.objects.filter to get messages
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class UserConversationsAPIView(APIView):
    """
    API view to get all conversations for the authenticated user
    """
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]  # Add IsAuthenticated here

    def get(self, request):
        conversations = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)


# If you need function-based views with decorators
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Add IsAuthenticated here
def user_messages(request):
    """
    Get all messages for the authenticated user
    """
    messages = Message.objects.filter(
        models.Q(sender=request.user) | 
        models.Q(conversation__participants=request.user)
    ).distinct().order_by('-timestamp')
    
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)