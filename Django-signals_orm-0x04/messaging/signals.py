from django.db.models.signals import post_delete, post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


# ------------------------------
# CLEANUP USER DATA ON DELETE
# ------------------------------
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


# ------------------------------
# CREATE NOTIFICATION ON NEW MESSAGE
# ------------------------------
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Automatically create a notification for the receiver when
    a new Message instance is created.
    """
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


# ------------------------------
# LOG MESSAGE HISTORY BEFORE EDIT
# ------------------------------
@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """
    Save the old content of a message to MessageHistory before it is updated.
    Also tracks who edited the message via _edited_by_user attribute.
    """
    if not instance.pk:
        return  # Skip if the message is new

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_instance.content != instance.content:
        # Mark message as edited
        instance.edited = True
        # Save history
        MessageHistory.objects.create(
            message=instance,
            old_content=old_instance.content,
            edited_by=getattr(instance, "_edited_by_user", None)
        )
