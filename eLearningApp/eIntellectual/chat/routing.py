# The provenance of the following code is from:  
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chatroom/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]