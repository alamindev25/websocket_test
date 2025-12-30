# livechart/serializers.py
from rest_framework import serializers
from .models import ChartData

class ChartDataSerializer(serializers.ModelSerializer):
    user_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ChartData
        fields = ['id', 'user', 'username', 'value', 'message', 'created_at', 'user_display']
        
    def get_user_display(self, obj):
        return obj.username or (obj.user.username if obj.user else 'Anonymous')
