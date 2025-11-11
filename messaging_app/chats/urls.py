from django.urls import path, include
import rest_framework.routers  # ✅ Import the routers module
from . import views

# Create a router and register our ViewSets
router = rest_framework.routers.DefaultRouter()  # ✅ Use routers.DefaultRouter()
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
   # path('', views.chats, name='chats_list'),
]