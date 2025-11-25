from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


# ------------------------------
#  CUSTOM MANAGER FOR UNREAD MESSAGES
# ------------------------------
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a specific user.
        Uses .only() to optimize query.
        """
        return (
            self.filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
            .select_related("sender")  # fast lookup of sender
        )


# ------------------------------
#  MESSAGE MODEL
# ------------------------------
class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    read = models.BooleanField(default=False)  # unread/read flag
    edited = models.BooleanField(default=False)  # track if edited
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )

    # Managers
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"Message {self.id} from {self.sender}"


# ------------------------------
#  NOTIFICATION MODEL
# ------------------------------
class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="notifications"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"


# ------------------------------
#  MESSAGE HISTORY MODEL
# ------------------------------
class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"


# ------------------------------
#  SIGNALS
# ------------------------------

# Create a notification when a new message is sent
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


# Log old content before a message is updated
@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if message is new
    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if old_instance.content != instance.content:
        # Mark message as edited
        instance.edited = True
        # Save history
        MessageHistory.objects.create(message=instance, old_content=old_instance.content)
