from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a specific user.
        Uses .only() to optimize query.
        """
        return (
            self.filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
            .select_related("sender")      # fast lookup of sender
        )


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    read = models.BooleanField(default=False)  # <-- NEW FIELD
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    # Default + custom managers
    objects = models.Manager()
    unread = UnreadMessagesManager()  # <-- CUSTOM MANAGER

    def __str__(self):
        return f"Message {self.id} from {self.sender}"
