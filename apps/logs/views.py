import logging
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
import pandas as pd

from .models import ImportStatus, FileUploadTrack
from .forms import FileUploadForm
from .tasks import process_file_upload

import logging
import pandas as pd
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from .models import ImportStatus
from apps.products.models import Product, ProductAdditionalImages, ProductShipping
from .utils import validate_row, create_product_from_row

logger = logging.getLogger('product_import')



# Create your views here.
def file_upload_view(request):
    form = FileUploadForm()
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        logger.info("Processing file upload request")
        if form.is_valid():
            try:
                file_track = form.save(commit=False)
                file_track.status = ImportStatus.PENDING
                file_track.save()
                logger.info(f"Created FileUploadTrack with ID: {file_track.id}")

                # Start the Celery task
                try:
                    task = process_file_upload.delay(str(file_track.id))
                    logger.info(f"Started Celery task with ID: {task.id}")
                    
                    messages.success(
                        request, 
                        f"File upload started. You can track the progress using the process ID: {file_track.id}"
                    )
                    return redirect('logs:file_upload_status', id=file_track.id)
                except Exception as e:
                    logger.exception(f"Failed to start Celery task: {str(e)}")
                    file_track.status = ImportStatus.FAILED
                    file_track.save()
                    messages.error(request, f"Failed to start file processing: {str(e)}")
                    return redirect(request.META.get('HTTP_REFERER', '/'))

            except Exception as e:
                logger.exception(f"Error in file upload view: {str(e)}")
                messages.error(request, f"Import failed: {str(e)}")
                return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            logger.error(f"Invalid form submission: {form.errors}")
            messages.error(request, "Invalid form submission.")

    return render(request, 'logs/upload_file.html', {'form': form})



def file_upload_status_view(request, id):
    file_track = get_object_or_404(FileUploadTrack, id=id)
    return render(request, 'logs/upload_status.html', {'file_track': file_track})

