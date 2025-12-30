from django.shortcuts import render

# Create your views here.
# livechart/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChartData
from .serializers import ChartDataSerializer

class ChartDataAPIView(APIView):

    def get(self, request):
        # Get user filter from query params
        user_id = request.query_params.get('user_id')
        username = request.query_params.get('username')
        
        queryset = ChartData.objects.order_by("-created_at")
        
        # Filter by user if specified
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        elif username:
            queryset = queryset.filter(username=username)
            
        # Limit to latest 20 records
        queryset = queryset[:20]
        
        serializer = ChartDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChartDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Automatically set user if authenticated
        if request.user.is_authenticated:
            instance = serializer.save(user=request.user)
        else:
            instance = serializer.save()

        # 🔥 WebSocket trigger with user info
        channel_layer = get_channel_layer()
        user_display = instance.username or (instance.user.username if instance.user else 'Anonymous')
        
        async_to_sync(channel_layer.group_send)(
            "live_chart",
            {
                "type": "send_chart_data",
                "data": {
                    "id": instance.id,
                    "value": instance.value,
                    "message": instance.message,
                    "time": instance.created_at.isoformat(),
                    "user": user_display
                }
            }
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageAPIView(APIView):
    """
    API endpoint specifically for sending messages
    """
    
    def post(self, request):
        # Extract message and username from request
        message = request.data.get('message')
        username = request.data.get('username', 'Anonymous')
        
        if not message:
            return Response(
                {"error": "Message is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new message entry
        data = {
            'message': message,
            'username': username
        }
        
        serializer = ChartDataSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Save with user if authenticated
        if request.user.is_authenticated:
            instance = serializer.save(user=request.user)
        else:
            instance = serializer.save()

        # 🔥 WebSocket trigger for message
        channel_layer = get_channel_layer()
        user_display = instance.username or (instance.user.username if instance.user else 'Anonymous')
        
        async_to_sync(channel_layer.group_send)(
            "live_chart",
            {
                "type": "send_chart_data",
                "data": {
                    "id": instance.id,
                    "message": instance.message,
                    "time": instance.created_at.isoformat(),
                    "user": user_display,
                    "type": "message"
                }
            }
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
