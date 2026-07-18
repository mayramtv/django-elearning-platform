# I write the following code following the following guidlines, documentation and classes
    # https://docs.djangoproject.com/en/5.1/
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan

from django.db import models
from management.models import User
from datetime import datetime  

# Chatroom Model : is a group of messages
class Chatroom(models.Model):
    name = models.CharField('Anonymous', max_length=100, blank=False, null=True)
    label = models.CharField(max_length=100, blank=True, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    photo = models.ImageField(upload_to='chatroom_images/', blank=True, null=True)

# Chat model: each chatroom can have many chats or messages
class Chat(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(blank=True, null=True)
