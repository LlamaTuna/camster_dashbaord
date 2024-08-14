from django.shortcuts import render
from rest_framework import viewsets
from .models import Event, VideoClip
from .serializers import EventSerializer, VideoClipSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from .serializers import LogSerializer
from .serializers import EventSerializer, VideoClipSerializer, LogSerializer
from rest_framework import status



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class VideoClipViewSet(viewsets.ModelViewSet):
    queryset = VideoClip.objects.all()
    serializer_class = VideoClipSerializer

from django.shortcuts import render
from .models import Event, VideoClip

@login_required
def index(request):
    logs = Event.objects.all().order_by('-timestamp')  # Get all logs, ordered by timestamp
    clips = VideoClip.objects.all().order_by('-created_at')  # Get all video clips, ordered by creation time

    context = {
        'logs': logs,
        'clips': clips,
    }
    return render(request, 'dashboard/index.html', context)


class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

@login_required
def index(request):
    return render(request, 'dashboard/index.html')

@api_view(['POST'])
def log_event(request):
    serializer = LogSerializer(data=request.data)
    if serializer.is_valid():
        Event.objects.create(
            name=serializer.validated_data['event_type'],
            description=serializer.validated_data['description']
            # extra_data should be stored if your model allows it
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
        
        # Get or create a default event
        default_event, created = Event.objects.get_or_create(name="Default Event", defaults={"description": "Default event for unassociated clips"})
        
        VideoClip.objects.create(
            event=default_event,
            file=video_file,
            description=description
        )
        return Response({"message": "Video received"}, status=status.HTTP_201_CREATED)
    return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)



def register(request):
    """
    Handles user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered register page with the form or a redirect to index.
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