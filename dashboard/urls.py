from django.urls import path
from .views import index, register, CustomLoginView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('api/log_event/', views.log_event, name='log_event'),
    path('api/upload_video/', views.upload_video, name='upload_video'),
]
