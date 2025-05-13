from django.contrib import admin
from .models import FileUploadTrack

# Register your models here.
@admin.register(FileUploadTrack)
class FileUploadTrackAdmin(admin.ModelAdmin):
    list_display = ['file', 'status', 'start_time', 'end_time', 'total_records', 'success_count', 'warning_count', 'failed_count']
    list_filter = ['status']
    search_fields = ['file']
    readonly_fields = ['start_time', 'end_time']
