# import models
from django.contrib import admin
from .models import Chat, Chatroom

class ChatroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'date_created', 'photo')


class ChatAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'chatroom', 'content')

admin.site.register(Chatroom, ChatroomAdmin) 
admin.site.register(Chat, ChatAdmin) 