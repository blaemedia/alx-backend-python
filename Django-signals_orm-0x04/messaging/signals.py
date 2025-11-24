from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(pre_save, sender=Message)
def save_old_message_content(sender, instance, **kwargs):
    # If message already exists (editing)
    if instance.id:
        old_message = Message.objects.get(id=instance.id)

        # Only save history if content is changing
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True   # Mark message as edited


@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    # Only notify on new messages, not edits
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
