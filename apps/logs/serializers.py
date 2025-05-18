from rest_framework import serializers
from .models import FileUploadTrack


class FileUploadTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploadTrack
        fields = [
            'file',
            'start_time',
            'end_time',
            'status',
            'total_records',
            'success_count',
            'warning_count',
            'failed_count',
        ]
