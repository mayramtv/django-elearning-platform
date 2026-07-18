# I write the following code following the following guidelines, documentation and classes
    # University of London Advance Web Development module
    # Lectures and Labs presented by Dr Daniel Buchan

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
