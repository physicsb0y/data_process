from django.db import models
import uuid
from apps.products.models import BaseModel

# Create your models here.
class ImportStatus(models.TextChoices):
    SUCCESS = 'Success', 'Success'
    FAILED = 'Failed', 'Failed'
    PENDING = 'Pending', 'Pending'
    PROCESSING = 'Processing', 'Processing'
    PARTIALLY_FAILED = 'Partially Failed', 'Partially Failed'



class FileUploadTrack(BaseModel):
    """Model to track the file upload"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=255, choices=ImportStatus.choices)
    total_records = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    warning_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)

    @property
    def total_time_taken(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None
    
    def __str__(self):
        return f"{self.file.name} - ({self.status})"
    