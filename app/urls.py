from django.urls import path

from . import views

urlpatterns = [
    path('', views.QueryVideos.as_view()),
]