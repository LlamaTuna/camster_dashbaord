from rest_framework import serializers
from .models import Event, VideoClip

class LogSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    event_type = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    extra_data = serializers.JSONField(required=False, allow_null=True)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class VideoClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoClip
        fields = '__all__'
