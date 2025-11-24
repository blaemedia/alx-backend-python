from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory


class MessageHistoryTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass123')
        self.receiver = User.objects.create_user(username='receiver', password='pass123')

    def test_message_edit_creates_history(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original message"
        )

        # Edit message
        message.content = "Updated message"
        message.save()

        history = MessageHistory.objects.filter(message=message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Original message")
        self.assertTrue(message.edited)
