from celery import shared_task
import pandas as pd
from django.db import transaction
from django.utils import timezone
import logging
from .models import FileUploadTrack, ImportStatus
from .utils import validate_row, create_product_from_row
import os

logger = logging.getLogger('product_import')

@shared_task
def process_file_upload(file_track_id):
    logger.info(f"Starting task for file_track_id: {file_track_id}")
    try:
        file_track = FileUploadTrack.objects.get(id=file_track_id)
        logger.info(f"Found file_track: {file_track.id}, file path: {file_track.file.path}")
        
        if not os.path.exists(file_track.file.path):
            logger.error(f"File does not exist at path: {file_track.file.path}")
            raise FileNotFoundError(f"File not found at {file_track.file.path}")

        file_path = file_track.file.path
        logger.info(f"Reading file: {file_path}")

        try:
            df = pd.read_excel(file_path) if file_path.endswith(('.xlsx', '.xls')) else pd.read_csv(file_path)
            logger.info(f"Successfully read file with {len(df)} rows")
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            raise

        file_track.total_records = len(df)
        file_track.save()

        chunk_size = 100
        total_success, total_errors, total_warnings = 0, 0, 0
        start_time = timezone.now()

        logger.info(f"Starting to process {len(df)} rows in chunks of {chunk_size}")
        for start in range(0, len(df), chunk_size):
            chunk = df.iloc[start:start + chunk_size]
            logger.info(f"Processing chunk {start//chunk_size + 1} of {(len(df) + chunk_size - 1)//chunk_size}")

            with transaction.atomic():
                for index, row in chunk.iterrows():
                    data = row.to_dict()
                    logger.info(f"Processing row {index + 1}")
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

            # Update status after each chunk
            file_track.success_count = total_success
            file_track.warning_count = total_warnings
            file_track.failed_count = total_errors
            file_track.save()
            logger.info(f"Chunk completed. Success: {total_success}, Warnings: {total_warnings}, Errors: {total_errors}")

        file_track.end_time = timezone.now()
        file_track.status = ImportStatus.SUCCESS if total_errors == 0 else ImportStatus.PARTIALLY_FAILED
        file_track.save()
        logger.info(f"Task completed. Final status: {file_track.status}")

    except Exception as e:
        logger.exception(f"Critical error in task: {str(e)}")
        if 'file_track' in locals():
            file_track.status = ImportStatus.FAILED
            file_track.save()
        raise 
