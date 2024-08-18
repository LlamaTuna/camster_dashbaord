from django.urls import path
from .views import index, register, CustomLoginView
from django.contrib.auth import views as auth_views
from . import views
from .views import index, delete_video, delete_all_videos, download_all_videos


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('api/log_event/', views.log_event, name='log_event'),
    path('api/upload_video/', views.upload_video, name='upload_video'),
    path('delete_video/<int:video_id>/', delete_video, name='delete_video'),
    path('delete_all_videos/', delete_all_videos, name='delete_all_videos'),
    path('download-all-videos/', download_all_videos, name='download_all_videos'),
]
