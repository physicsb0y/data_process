from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import FileUploadTrack
from .serializers import FileUploadTrackSerializer

class FileUploadStatusView(generics.RetrieveAPIView):
    """
    API view to get the status of a file upload task
    """
    queryset = FileUploadTrack.objects.all()
    serializer_class = FileUploadTrackSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'id': str(instance.id),
                'status': instance.status,
                'total_records': instance.total_records,
                'success_count': instance.success_count,
                'warning_count': instance.warning_count,
                'failed_count': instance.failed_count,
                'start_time': instance.start_time,
                'end_time': instance.end_time,
                'total_time_taken': instance.total_time_taken
            })
        
        except FileUploadTrack.DoesNotExist:
            return Response(
                {'error': 'File upload task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
