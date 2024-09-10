from django.urls import path
from .views import index, register, CustomLoginView
from django.contrib.auth import views as auth_views
from . import views
from .views import index, delete_video, delete_all_videos, download_all_videos, delete_selected_events

# URL patterns that map specific URL paths to corresponding views within the app.
urlpatterns = [
    path('', index, name='index'),
    # The home page of the application, handled by the 'index' view.

    path('register/', register, name='register'),
    # The user registration page, handled by the 'register' view.

    path('accounts/login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    # The user login page, using Django's built-in LoginView but customized with a template from 'dashboard/login.html'.

    path('api/log_event/', views.log_event, name='log_event'),
    # API endpoint to log events, handled by the 'log_event' view.

    path('api/upload_video/', views.upload_video, name='upload_video'),
    # API endpoint for uploading videos, handled by the 'upload_video' view.

    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),
    # URL pattern to delete a specific video by its 'video_id', handled by the 'delete_video' view.

    path('delete_all_videos/', delete_all_videos, name='delete_all_videos'),
    # URL pattern to delete all videos, handled by the 'delete_all_videos' view.

    path('download-all-videos/', download_all_videos, name='download_all_videos'),
    # URL pattern to download all videos as a batch, handled by the 'download_all_videos' view.

    path('delete_selected_events/', delete_selected_events, name='delete_selected_events'),
    # URL pattern to delete selected events, handled by the 'delete_selected_events' view.
]
