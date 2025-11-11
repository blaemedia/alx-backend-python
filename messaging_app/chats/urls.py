from django.urls import path, include
import rest_framework.routers  
from rest_framework_nested import routers as nested_routers
from . import views

# Create a router and register our ViewSets
router = rest_framework.routers.DefaultRouter()  
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)

# Create nested router for messages
conversations_router = nested_routers.NestedDefaultRouter(
    router, r'conversations', lookup='conversation'
)
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
   # path('', views.chats, name='chats_list'),
]