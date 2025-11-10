# Create your models here.
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add additional fields not in built-in User model
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    
    # Add any other custom fields you need
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'auth_user'  # Optional: to use existing auth_user table if migrating

    def __str__(self):
        return self.username
    

# models.py
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-updated_at']
        db_table = 'conversations'

    def __str__(self):
        if self.is_group:
            return f"Group: {self.group_name}"
        participants = self.participants.all()
        return f"Conversation between {', '.join([user.username for user in participants])}"
    
# models.py
class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # Optional: For file/image sharing
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    attachment_type = models.CharField(
        max_length=10, 
        choices=[
            ('image', 'Image'),
            ('file', 'File'),
            ('audio', 'Audio'),
            ('video', 'Video')
        ], 
        blank=True, 
        null=True
    )
    
    class Meta:
        ordering = ['timestamp']
        db_table = 'messages'

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"