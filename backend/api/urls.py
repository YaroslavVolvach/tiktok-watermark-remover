from django.urls import path
from .views import UploadVideoView, RetrieveVideoView

urlpatterns = [
    path('upload/', UploadVideoView.as_view(), name='upload-video'),
    path('videos/<int:video_id>/', RetrieveVideoView.as_view(), name='retrieve-video'),
]