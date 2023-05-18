from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

class Video(models.Model):
    title = models.CharField(max_length=100)
    # your other fields...
    video_file = models.FileField(upload_to='videos', storage=S3Boto3Storage())
    # ...
    

class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField()

