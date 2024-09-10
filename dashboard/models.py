from django.db import models

class Event(models.Model):
    """
    A model representing an event with an associated name, timestamp, and description.
    
    The Event model captures a specific occurrence, including its name, the time it occurred,
    a description, and optionally the name of a recognized face associated with the event.
    """

    name = models.CharField(max_length=100)
    # The name of the event, limited to 100 characters.
    
    timestamp = models.DateTimeField(auto_now_add=True)
    # The timestamp when the event is created. Automatically set to the current date and time.
    
    description = models.TextField()
    # A detailed description of the event.
    
    named_face = models.CharField(max_length=255, null=True, blank=True)
    # Optionally stores the name of a recognized face related to the event.
    # The field can be empty (blank) or null.

    def __str__(self):
        """
        Returns a string representation of the Event, which will be the event's name.
        """
        return self.name

class VideoClip(models.Model):
    """
    A model representing a video clip associated with an event.
    
    The VideoClip model stores a file representing a video clip, metadata about the clip (event, 
    creation date, optional thumbnail), and an optional description of the clip.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='clips')
    # A foreign key linking the video clip to a specific event. If the event is deleted, 
    # all related video clips are also deleted.
    
    file = models.FileField(upload_to='clips/')
    # The video file associated with the event. Uploaded to the 'clips/' directory.
    
    created_at = models.DateTimeField(auto_now_add=True)
    # The timestamp when the video clip was created. Automatically set to the current date and time.
    
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    # An optional thumbnail image for the video clip. Uploaded to the 'thumbnails/' directory. 
    # The field can be empty or null.
    
    description = models.TextField(blank=True, null=True)
    # An optional text description of the video clip.

    def __str__(self):
        """
        Returns a string representation of the VideoClip, which includes the event name 
        and the creation timestamp of the clip.
        """
        return f"Clip for {self.event.name} at {self.created_at}"
