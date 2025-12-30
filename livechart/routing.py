from django.urls import re_path
from .consumers import LiveChartConsumer

websocket_urlpatterns = [
    re_path(r"live-chart/$", LiveChartConsumer.as_asgi()),
]
