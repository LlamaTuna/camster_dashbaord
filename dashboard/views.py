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

class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

@api_view(['POST'])
def log_event(request):
    serializer = LogSerializer(data=request.data)
    if serializer.is_valid():
        Event.objects.create(
            name=serializer.validated_data['event_type'],
            description=serializer.validated_data['description'],
            timestamp=serializer.validated_data['timestamp']
            # Add extra_data if the model allows it
        )
        return Response({"message": "Log received"}, status=201)
    else:
        print(f"Invalid log event data: {serializer.errors}")
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def upload_video(request):
    video_file = request.FILES.get('video')
    if video_file:
        description = request.data.get('description', 'No description provided')
        
        default_event, created = Event.objects.get_or_create(
            name="Default Event", 
            defaults={"description": "Default event for unassociated clips"}
        )
        
        VideoClip.objects.create(
            event=default_event,
            file=video_file,
            # Assuming 'description' exists on the model
            description=description
        )
        return Response({"message": "Video received"}, status=status.HTTP_201_CREATED)
    return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)

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
