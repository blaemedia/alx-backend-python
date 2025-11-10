# messaging_app/models.py
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = 'guest', _('Guest')
        HOST = 'host', _('Host')
        ADMIN = 'admin', _('Admin')
    
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
        default=Role.GUEST,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    participants = models.ManyToManyField(
        User, 
        related_name='conversations',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        participant_names = [f"{user.first_name} {user.last_name}" 
                           for user in self.participants.all()]
        return f"Conversation: {', '.join(participant_names)}"

class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages',
        db_index=True
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        db_index=True
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['sent_at']),
            models.Index(fields=['sender', 'conversation']),
        ]

    def __str__(self):
        return f"Message from {self.sender.first_name} at {self.sent_at}"