
from django.urls import path
from . import auth, drive
from .views import MessageListView, SendMessageAPI

urlpatterns = [
    path('auth/start/', auth.start_google_auth, name='start_google_auth'),
    path('auth/callback/', auth.google_auth_callback, name='google_auth_callback'),

    path('drive/connect/', drive.connect_google_drive, name='connect_google_drive'),
    path('drive/callback/', drive.drive_callback, name='drive_callback'),
    path('drive/files/', drive.list_drive_files, name='list_drive_files'),
    path('drive/upload/', drive.upload_file_to_drive, name='upload_file_to_drive'),
    path('drive/download/<str:file_id>/', drive.download_file_from_drive, name='download_file_from_drive'),
    path('messages/', MessageListView.as_view()),
    path('send-message/', SendMessageAPI.as_view(), name='send_message'),
]
