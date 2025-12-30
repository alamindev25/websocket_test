# livechart/urls.py
from django.urls import path
from .views import ChartDataAPIView, MessageAPIView

urlpatterns = [
    path("chart-data/", ChartDataAPIView.as_view()),
    path("messages/", MessageAPIView.as_view()),
]
