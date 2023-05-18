from django.contrib import admin
from django.urls import path, include
from videos.views import VideoListView, home_view, upload_video, video_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('', home_view, name='home'),
    path('videos/upload/', upload_video, name='upload_video'),
    path('videos/', include('videos.urls', namespace='videos')),
    path('videos/upload/', video_upload, name='upload_video'),
    
]
