from rest_framework import serializers
from .models import Event, VideoClip

class LogSerializer(serializers.Serializer):
    """
    A serializer for logging events in a structured format.
    
    The LogSerializer allows the creation and validation of log entries containing
    a timestamp, event type, description, and optional extra data in JSON format.
    """

    timestamp = serializers.DateTimeField()
    # The date and time when the event occurred.
    
    event_type = serializers.CharField(max_length=100)
    # The type or category of the event (e.g., "info", "warning", etc.), limited to 100 characters.
    
    description = serializers.CharField(max_length=255)
    # A brief description of the event, limited to 255 characters.
    
    extra_data = serializers.JSONField(required=False)
    # Additional optional data related to the event, stored as JSON. This field is not required.

class EventSerializer(serializers.ModelSerializer):
    """
    A serializer for the Event model.
    
    The EventSerializer automatically serializes all fields of the Event model,
    allowing easy conversion between Event instances and JSON format for API responses.
    """

    class Meta:
        """
        Meta class that defines the model and fields for the EventSerializer.
        
        The serializer is linked to the Event model, and all fields are included 
        in the serialized representation.
        """
        model = Event
        fields = '__all__'
        # Includes all fields of the Event model in the serialized output.

class VideoClipSerializer(serializers.ModelSerializer):
    """
    A serializer for the VideoClip model.
    
    The VideoClipSerializer handles the conversion of VideoClip instances 
    to and from JSON format, including all fields of the model.
    """

    class Meta:
        """
        Meta class that defines the model and fields for the VideoClipSerializer.
        
        The serializer is linked to the VideoClip model, and all fields are included
        in the serialized representation.
        """
        model = VideoClip
        fields = '__all__'
        # Includes all fields of the VideoClip model in the serialized output.
