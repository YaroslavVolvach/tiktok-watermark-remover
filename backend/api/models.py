from django.db import models

class Video(models.Model):
    original_file = models.FileField(upload_to='videos/')
    processed_file = models.FileField(upload_to='processed/', blank=True, null=True)
    watermark_detected = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_file.name} (Detected: {self.watermark_detected})"