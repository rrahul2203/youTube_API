import logging
import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from youtube_API.settings import API_KEYS
from youtube_API.celery import app

from .models import Videos

logger = logging.getLogger(__name__)

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

#@app.task
def get_latest_videos(search = 'Cricket'):
    time_now = datetime.now()
    last_request_time = time_now - timedelta(minutes=1)
    developer_key = random.choice(API_KEYS)
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=developer_key)
    try:
        search_response = youtube.search().list(
            q=search, 
            part="id, snippet", 
            order="date", 
            maxResults=50, 
            publishedAfter=(last_request_time.replace(microsecond=0).isoformat()+'Z')
        )
    except HttpError as e:
        logger.error("An HTTP error {} occurred: {}".format(e.resp.status, e.content))

    try:
        created_videos = []
        for item in search_response.execute().get('items', []):
            video_id = item['id']['videoId']
            channel_id = item['snippet']['channelId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            channel_title = item['snippet']['channelTitle']
            thumbnail_url = item['snippet']['thumbnails']['default']['url']
            publish_time = item['snippet']['publishedAt']
            created_videos.append(
                Videos(
                    video_id=video_id,
                    channel_id=channel_id,
                    title=title,
                    description=description,
                    channel_title=channel_title,
                    thumbnail_url=thumbnail_url,
                    publish_time=publish_time,
                )
            )
        if created_videos:
            Videos.objects.bulk_create(created_videos, ignore_conflicts=True)
        logger.info("Successfully Created the video objects")
    except Exception as e:
        logger.error("Error: {} occured while creating the video objects.".format(e))
    




