# I write the following code following the following guidelines, documentation and classes
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan

from django.shortcuts import render
from .models import *

def lobby(request):
    return render(request, 'chat/lobby.html', {'data': "Chat lobby Page"})


def chatroom(request, name):
    chats = Chat.objects.filter(chatroom__name=name)
    return render(request, 'chat/chatroom.html', {'name': name, 'chats': chats })
