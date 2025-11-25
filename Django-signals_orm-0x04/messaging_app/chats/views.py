from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# NEW: cache imports
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer, ConversationDetailSerializer
from .auth import JWTAuth, MessageJWTAuth
from .pagination import CustomPagination
from .filters import MessageFilter, ConversationFilter


class ConversationViewSet(viewsets.ModelViewSet):
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants__username', 'participants__email']
    ordering_fields = ['last_message_timestamp', 'created_at']
    ordering = ['-last_message_timestamp']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer

    # -----------------------------------------
    # CACHE conversation messages endpoint
    # -----------------------------------------
    @action(detail=True, methods=['get'])
    @method_decorator(cache_page(60))   # <-- cache for 60 seconds
    def messages(self, request, pk=None):
        conversation = self.get_object()
        
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
        filtered_messages = MessageFilter(request.GET, queryset=messages).qs
        
        page = self.paginate_queryset(filtered_messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(filtered_messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        
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
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['content']
    ordering_fields = ['timestamp', 'id']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) | 
            models.Q(conversation__participants=self.request.user)
        ).distinct().select_related('sender', 'conversation')

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation_id')
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            if self.request.user not in conversation.participants.all():
                return Response(
                    {"detail": "You are not a participant in this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer.save(sender=self.request.user, conversation=conversation)
        else:
            serializer.save(sender=self.request.user)


class ConversationMessagesAPIView(APIView):
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]

    # -----------------------------------------
    # Optionally cache this too (based on ALX requirement)
    # -----------------------------------------
    @method_decorator(cache_page(60))
    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        messages = Message.objects.filter(conversation=conversation)
        filtered_messages = MessageFilter(request.GET, queryset=messages).qs.order_by('-timestamp')
        
        paginator = CustomPagination()
        paginated_messages = paginator.paginate_queryset(filtered_messages, request, view=self)
        serializer = MessageSerializer(paginated_messages, many=True)
        
        return paginator.get_paginated_response(serializer.data)


class UserConversationsAPIView(APIView):
    authentication_classes = JWTAuth.authentication_classes
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = Conversation.objects.filter(participants=request.user)
        filtered_conversations = ConversationFilter(request.GET, queryset=conversations).qs
        ordering = request.GET.get('ordering', '-last_message_timestamp')
        if ordering.lstrip('-') in ['last_message_timestamp', 'created_at', 'id']:
            filtered_conversations = filtered_conversations.order_by(ordering)
        
        paginator = CustomPagination()
        paginated_conversations = paginator.paginate_queryset(filtered_conversations, request, view=self)
        serializer = ConversationSerializer(paginated_conversations, many=True)
        
        return paginator.get_paginated_response(serializer.data)


from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_messages(request):
    messages = Message.objects.filter(
        models.Q(sender=request.user) | 
        models.Q(conversation__participants=request.user)
    ).distinct()
    
    filtered_messages = MessageFilter(request.GET, queryset=messages).qs.order_by('-timestamp')
    
    paginator = CustomPagination()
    paginated_messages = paginator.paginate_queryset(filtered_messages, request)
    serializer = MessageSerializer(paginated_messages, many=True)
    
    if paginated_messages is not None:
        return paginator.get_paginated_response(serializer.data)
    
    serializer = MessageSerializer(filtered_messages, many=True)
    return Response(serializer.data)
