from django.urls import path
from . import views, api_view

app_name = 'logs'

urlpatterns = [
    path('', views.file_upload_view, name='file_upload'),
    path('status/<uuid:id>/', views.file_upload_status_view, name='file_upload_status'),
    path('api/file-upload/<uuid:id>/', api_view.FileUploadStatusView.as_view(), name='file_upload_status_api'),
]
