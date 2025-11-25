# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a specific user.
        Optimized with .only() to fetch only necessary fields and select_related
        for fast access to sender data.
        """
        return (
            self.get_queryset()
                .filter(receiver=user, read=False)
                .only("id", "sender", "content", "timestamp")
                .select_related("sender")
        )
