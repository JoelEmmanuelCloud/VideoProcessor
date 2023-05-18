from django.urls import path
from .views import video_list, video_upload, upload_video

app_name = 'videos'

urlpatterns = [
    path('', video_list, name='video_list'),
    path('upload/', video_upload, name='video_upload'),
    path('upload_video/', upload_video, name='upload_video'),
    
]
