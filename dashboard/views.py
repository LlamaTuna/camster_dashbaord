from django.shortcuts import render, redirect, get_object_or_404
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
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import zipfile

logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the Event model.
    
    Provides default CRUD (Create, Read, Update, Delete) operations for Event instances
    via the Django REST framework's ModelViewSet.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class VideoClipViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the VideoClip model.
    
    Provides default CRUD operations for VideoClip instances.
    """
    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer

@login_required
def index(request):
    """
    The home page view that displays all events and video clips.
    
    This view is only accessible to logged-in users. It retrieves all Event and VideoClip objects,
    orders them by timestamp and creation date, and renders them in the 'index.html' template.
    """
    events = Event.objects.all().order_by('-timestamp')
    video_clips = VideoClip.objects.all().order_by('-created_at')
    
    context = {
        'events': events,
        'video_clips': video_clips,
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def delete_video(request, video_id):
    """
    Deletes a video clip and its associated thumbnail, if they exist.
    
    This view finds a VideoClip by its ID, deletes the corresponding video and thumbnail files from the filesystem,
    and removes the VideoClip object from the database. Redirects to the index page after deletion.
    """
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
    """
    A custom login view using a custom template.
    
    This view extends Django's built-in LoginView, specifying 'dashboard/login.html'
    as the template for rendering the login form.
    """
    template_name = 'dashboard/login.html'

@login_required
def delete_all_videos(request):
    """
    Deletes all video clips and their associated thumbnails.
    
    This view iterates over all VideoClip objects, deletes their video and thumbnail files from the filesystem,
    and then deletes the VideoClip objects themselves. Only handles POST requests.
    """
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
    """
    API endpoint to log an event.
    
    This view handles POST requests to log events. It accepts a JSON payload containing the event type,
    description, and optional extra data such as the name of a recognized face. It creates an Event object
    and returns a response indicating success or failure.
    """
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
    """
    Generates a thumbnail for a video file.
    
    This function captures the first frame of the video at 'video_path', resizes it to the given size,
    and saves the resulting image to 'thumbnail_path'.
    """
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    if success:
        # Resize the frame
        resized_frame = cv2.resize(frame, size)
        cv2.imwrite(thumbnail_path, resized_frame)
    cap.release()

@api_view(['POST'])
def upload_video(request):
    """
    API endpoint to upload a video and generate a thumbnail.
    
    This view handles POST requests to upload a video file. It creates a VideoClip object,
    generates a thumbnail for the video, and returns a success response along with the video clip ID.
    """
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
    """
    Downloads all video clips as a ZIP file.
    
    This view compresses all video files into a ZIP archive and sends it as a downloadable file
    to the user. The ZIP file is generated dynamically in memory.
    """
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
    """
    User registration view.
    
    This view handles the user registration process. It renders a registration form,
    validates the form data, creates a new user, and logs them in. If the request method is GET,
    it displays the form. If POST, it processes the form data.
    """
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
    """
    Deletes selected events based on user input.
    
    This view handles POST requests to delete multiple selected events. It retrieves the selected
    event IDs from the POST data and deletes the corresponding Event objects. Redirects to the index page after deletion.
    """
    if request.method == 'POST':
        selected_events = request.POST.getlist('selected_events')
        if selected_events:
            Event.objects.filter(id__in=selected_events).delete()
        return redirect('index')  # Redirect back to the index page after deletion
    return HttpResponseRedirect(reverse('index'))
