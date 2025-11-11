from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet)
router.register(r'messages', views.MessageViewSet)




urlpatterns = [
    path('api/', include(router.urls)),
   # path('', views.chats, name='chats_list'),
]