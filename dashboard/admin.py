from django.contrib import admin
from .models import Event, VideoClip
from django.utils.html import format_html

# Register your models here
admin.site.register(Event)


class VideoClipAdmin(admin.ModelAdmin):
    list_display = ('event', 'created_at', 'thumbnail_preview')

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 50px; height: auto;">', obj.thumbnail.url)
        return "No thumbnail"

    thumbnail_preview.short_description = 'Thumbnail'

admin.site.register(VideoClip, VideoClipAdmin)
