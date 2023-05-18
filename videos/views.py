from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView
from .models import Video
from .ccextractor import extract_subtitles
from videos.models import Video
import boto3
from boto3.dynamodb.conditions import Key
from .forms import VideoForm


def video_detail(request, video_id):
    # Retrieve the video object from the database
    video = Video.objects.get(id=video_id)

    # Access the URL of the video file
    video_url = video.video_file.url

    # Pass the video URL to the template or perform further processing
    context = {
        'video_url': video_url
    }
    return render(request, 'video_detail.html', context)

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('video-list')
    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_upload(request):
    if request.method == 'POST':
        # Logic to handle the uploaded video file
        # ...
        return HttpResponse('Video uploaded successfully!')
    else:
        return render(request, 'video_upload.html')

def process_video(video_id):
    # Extract subtitles for video
    video = Video.objects.get(id=video_id)
    extract_subtitles(video.video_file.path)
    with open('subtitles.srt', 'r') as f:
        subtitle_text = f.read()
        # Save subtitles to DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('subtitle_table')
        table.put_item(
            Item={
                'video_id': str(video.id),
                'text': subtitle_text
            }
        )
    # Save processed video to S3
    s3 = boto3.client('s3')
    bucket_name = 'mytube-processed-videos'
    key = str(video.id) + '.mp4'
    s3.upload_file(video.video_file.path, bucket_name, key)

class VideoListView(ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'

    def get_queryset(self):
        videos = super().get_queryset()
        for video in videos:
            process_video(video.id)
        return videos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('keyword')
        if keyword:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('subtitle_table')
            response = table.scan(
                FilterExpression=Key('text').contains(keyword),
            )
            segments = response.get('Items', [])
            context['segments'] = segments
        return context
