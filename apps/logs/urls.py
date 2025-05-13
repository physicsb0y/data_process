from django.urls import path

from . import views

app_name = 'logs'

urlpatterns = [
    path('', views.file_upload_view, name='file_upload')
]
