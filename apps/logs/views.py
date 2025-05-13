import logging
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import pandas as pd

from .models import ImportStatus
from .forms import FileUploadForm


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
    print("GOT HERE: ")
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_track = form.save(commit=False)
            file_track.status = ImportStatus.PROCESSING
            file_track.save()

            try:
                file_path = file_track.file.path

                df = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(file_path)
                file_track.total_records = len(df)
                file_track.save()

                chunk_size = 100
                total_success, total_errors, total_warnings = 0, 0, 0
                start_time = timezone.now()

                for start in range(0, len(df), chunk_size):
                    chunk = df.iloc[start:start + chunk_size]

                    with transaction.atomic():
                        for index, row in chunk.iterrows():
                            data = row.to_dict()
                            logger.info("Data : %s", data)
                            errors, warnings = validate_row(data)

                            if errors:
                                total_errors += 1
                                logger.error(f"Row {index + 1}: {errors}")
                                continue

                            try:
                                create_product_from_row(data, file_track)
                                total_success += 1
                                if warnings:
                                    total_warnings += 1
                                    logger.warning(f"Row {index + 1}: {warnings}")
                            except Exception as e:
                                total_errors += 1
                                logger.error(f"Row {index + 1} failed: {str(e)}")

                file_track.success_count = total_success
                file_track.warning_count = total_warnings
                file_track.failure_count = total_errors
                file_track.end_time = timezone.now()
                file_track.status = ImportStatus.SUCCESS
                file_track.save()

                messages.success(request, f"File processed. Success: {total_success}, Warnings: {total_warnings}, Errors: {total_errors}")

            except Exception as e:
                logger.exception(f"Critical error: {str(e)}")
                file_track.status = ImportStatus.FAILED
                file_track.save()
                messages.error(request, f"Import failed: {str(e)}")
                return redirect(request.META.get('HTTP_REFERER', '/'))

        else:
            messages.error(request, "Invalid form submission.")

    return render(request, 'logs/upload_file.html', {'form': form})

