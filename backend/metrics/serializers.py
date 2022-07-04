from rest_framework import serializers
from .models import Metrics, Notifications

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'