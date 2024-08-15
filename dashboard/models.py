from django.db import models



class Event(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    named_face = models.CharField(max_length=255, null=True, blank=True)  # Add this field

    def __str__(self):
        return self.name

class VideoClip(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='clips')
    file = models.FileField(upload_to='clips/')
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Add this line

    def __str__(self):
        return f"Clip for {self.event.name} at {self.created_at}"

