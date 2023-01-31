from django.db import models

class Videos(models.Model):
    id = models.BigAutoField(primary_key=True)
    video_id = models.CharField(null=False, blank=False, max_length=200)
    channel_id = models.CharField(null=False, blank=False, max_length=500)
    title = models.CharField(null=True, blank=True, max_length=500)
    description = models.CharField(null=True, blank=True, max_length=5000)
    channel_title = models.CharField(null=True, blank=True, max_length=500)
    thumbnail_url = models.URLField()
    publish_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "videos"


