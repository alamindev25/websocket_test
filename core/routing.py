from django.urls import re_path
from channels.routing import URLRouter
from livechart.routing import websocket_urlpatterns as livechart_ws

websocket_urlpatterns = [
    re_path(r"ws/", URLRouter(livechart_ws)),
]
