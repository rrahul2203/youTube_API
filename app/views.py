from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Videos
from .serializer import VideosSerializer


# # Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class QueryVideos(ListAPIView):
    default_limit=20
    max_limit = 100
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter)
    filterset_fields = ['channel_id','channel_title']
    ordering = ('-publish_time')
    pagination_class = StandardResultsSetPagination


    