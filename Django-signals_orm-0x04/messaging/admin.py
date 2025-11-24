from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'edited', 'timestamp', 'updated_at')
    search_fields = ('sender__username', 'receiver__username', 'content')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'timestamp')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'edited_at')
    search_fields = ('message__content',)
