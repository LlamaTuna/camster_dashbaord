from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Event, VideoClip
from .serializers import EventSerializer, VideoClipSerializer, LogSerializer
from .forms import CustomUserCreationForm
import cv2
import os
from django.conf import settings
import logging 
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import zipfile


logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class VideoClipViewSet(viewsets.ModelViewSet):
    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer

@login_required
def index(request):
    events = Event.objects.all().order_by('-timestamp')
    video_clips = VideoClip.objects.all().order_by('-created_at')
    
    context = {
        'events': events,
        'video_clips': video_clips,
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def delete_video(request, video_id):
    clip = get_object_or_404(VideoClip, id=video_id)
    
    # Delete the thumbnail file if it exists
    if clip.thumbnail and os.path.isfile(clip.thumbnail.path):
        os.remove(clip.thumbnail.path)
    
    # Delete the video file if it exists
    if clip.file and os.path.isfile(clip.file.path):
        os.remove(clip.file.path)
    
    # Delete the VideoClip object
    clip.delete()
    
    return HttpResponseRedirect(reverse('index'))


class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

@login_required
def delete_all_videos(request):
    if request.method == 'POST':
        # Get all video clips
        clips = VideoClip.objects.all()

        for clip in clips:
            # Delete the thumbnail file if it exists
            if clip.thumbnail and os.path.isfile(clip.thumbnail.path):
                os.remove(clip.thumbnail.path)
            
            # Delete the video file if it exists
            if clip.file and os.path.isfile(clip.file.path):
                os.remove(clip.file.path)

            # Delete the VideoClip object
            clip.delete()

        return HttpResponseRedirect(reverse('index'))

    return HttpResponse(status=405)  # Method not allowed for GET requests


@api_view(['POST'])
def log_event(request):
    serializer = LogSerializer(data=request.data)
    if serializer.is_valid():
        # Extract extra_data if present
        extra_data = serializer.validated_data.get('extra_data', {})
        face_name = extra_data.get('face_name')

        # Save event with the named face if provided
        event = Event.objects.create(
            name=serializer.validated_data['event_type'],
            description=serializer.validated_data['description'],
            named_face=face_name  # Save the named face here
        )

        if face_name:
            print(f"Detected face: {face_name}")
        
        return Response({"message": "Log received"}, status=status.HTTP_201_CREATED)
    else:
        print(f"Invalid log event data: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def generate_thumbnail(video_path, thumbnail_path, size=(220, 140)):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    if success:
        # Resize the frame
        resized_frame = cv2.resize(frame, size)
        cv2.imwrite(thumbnail_path, resized_frame)
    cap.release()

@api_view(['POST'])
def upload_video(request):
    logger.info(f"Request data: {request.data}")
    video_file = request.FILES.get('video')
    if video_file:
        description = request.data.get('description', 'No description provided')

        default_event, created = Event.objects.get_or_create(
            name="Default Event", 
            defaults={"description": "Default event for unassociated clips"}
        )

        video_clip = VideoClip.objects.create(
            event=default_event,
            file=video_file,
            description=description,
        )

        # Generate a thumbnail
        video_path = video_clip.file.path
        thumbnail_filename = f'{video_clip.id}.jpg'
        thumbnail_path = os.path.join('thumbnails', thumbnail_filename)
        full_thumbnail_path = os.path.join(settings.MEDIA_ROOT, thumbnail_path)
        generate_thumbnail(video_path, full_thumbnail_path)

        # Update the video clip with the relative thumbnail path
        video_clip.thumbnail = thumbnail_path
        video_clip.save()
        
        return Response({"message": "Video and thumbnail received", "video_clip_id": video_clip.id}, status=status.HTTP_201_CREATED)

    return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)

def download_all_videos(request):
    # Define the zip file name
    zip_filename = "all_videos.zip"

    # Create the zip file in memory
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={zip_filename}'

    with zipfile.ZipFile(response, 'w') as zip_file:
        # Add each video file to the zip file
        for clip in VideoClip.objects.all():
            video_path = os.path.join(settings.MEDIA_ROOT, clip.file.name)
            zip_file.write(video_path, os.path.basename(video_path))

    return response

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'dashboard/register.html', {'form': form})

@login_required
def delete_selected_events(request):
    if request.method == 'POST':
        selected_events = request.POST.getlist('selected_events')
        if selected_events:
            Event.objects.filter(id__in=selected_events).delete()
        return redirect('index')  # Redirect back to the index page after deletion
    return HttpResponseRedirect(reverse('index'))