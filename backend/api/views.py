import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Video
from api.services.video_processing import detect_tiktok_watermark, remove_watermark

class UploadVideoView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('video')

        if not file_obj:
            return Response({"error": "No video file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        media_path = settings.MEDIA_ROOT
        os.makedirs(os.path.join(media_path, 'videos'), exist_ok=True)
        os.makedirs(os.path.join(media_path, 'processed'), exist_ok=True)

        video = Video.objects.create(
            original_file=file_obj,
        )

        original_path = os.path.join(settings.MEDIA_ROOT, video.original_file.name)
        processed_filename = f"processed_{os.path.basename(video.original_file.name)}"
        processed_path = os.path.join(settings.MEDIA_ROOT, 'processed', processed_filename)

        watermark_detected = detect_tiktok_watermark(original_path)
        remove_watermark(original_path, processed_path)

        video.watermark_detected = watermark_detected
        with open(processed_path, 'rb') as f:
            video.processed_file.save(processed_filename, f, save=True)

        return Response({
            "message": "Video uploaded and processed successfully!",
            "id": video.id,
            "original_filename": video.original_file.name,
            "original_video_url": video.original_file.url,
            "processed_video_url": video.processed_file.url,
            "watermark_detected": video.watermark_detected
        }, status=status.HTTP_201_CREATED)

class RetrieveVideoView(APIView):
    def get(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(Video, id=video_id)

        return Response({
            "id": video.id,
            "original_filename": video.original_file.name,
            "original_video_url": video.original_file.url if video.original_file else None,
            "processed_video_url": video.processed_file.url if video.processed_file else None,
            "watermark_detected": video.watermark_detected,
            "uploaded_at": video.uploaded_at
        }, status=status.HTTP_200_OK)