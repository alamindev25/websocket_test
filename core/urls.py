"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

# core/urls.py
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import render

def test_websocket_view(request):
    with open('test_websocket.html', 'r') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html')

def multi_user_chat_view(request):
    with open('multi_user_chat.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html')

urlpatterns = [
    path("api/", include("livechart.urls")),
    path("test/", test_websocket_view, name="test_websocket"),
    path("chat/", multi_user_chat_view, name="multi_user_chat"),
]
