from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Automatically clean up messages, notifications, and histories
    when a user account is deleted.
    """

    # Delete messages the user sent
    Message.objects.filter(sender=instance).delete()

    # Delete messages the user received
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications addressed to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories created from messages linked to this user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
