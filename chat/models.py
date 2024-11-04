from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contact')
    profile = models.ImageField(upload_to='images/', default='images/placeholder.jfif')
    phone_number = models.CharField(blank=True, max_length=15, null=True, default='images/placeholder.jfif')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)  # Ensure the name is unique
    members = models.ManyToManyField(Contact, related_name="chat_rooms")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Chat Room"
        verbose_name_plural = "Chat Rooms"


class Conversation(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='conversations')
    participants = models.ManyToManyField(Contact, related_name='conversations')
    started_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation in {self.chat_room.name} started on {self.started_at}"

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ["-started_at"]


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.sender.user.username + ' ' + self.message if self.sender else "Unknown sender"

    def clean(self):
        if not self.message and not self.image:
            raise ValidationError('Either content or image must be provided.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Messages'
        verbose_name_plural = 'Messages'
