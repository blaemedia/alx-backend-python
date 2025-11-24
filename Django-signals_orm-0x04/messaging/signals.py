from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(pre_save, sender=Message)
def save_old_message_content(sender, instance, **kwargs):

    if instance.id:
        old_message = Message.objects.get(id=instance.id)

        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True

            # If no editor is set (e.g. system update), keep old value
            if instance.edited_by is None:
                instance.edited_by = old_message.edited_by


@receiver(post_save, sender=Message)
def create_notification_for_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
