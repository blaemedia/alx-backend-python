from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages for the given user.
        Optimized with .only() to fetch only necessary fields.
        """
        return self.filter(receiver=user, read=False).only(
            'id', 'sender', 'content', 'timestamp'
        )


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    content = models.TextField()
    read = models.BooleanField(default=False)   # <-- New field
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="edited_messages"
    )
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE,
        related_name="replies"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"Message {self.id} from {self.sender}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID: {self.message.id}"
