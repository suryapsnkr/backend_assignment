from django.urls import path
from .views import send_whatsapp_message, whatsapp_webhook

urlpatterns = [
    path('send/', send_whatsapp_message, name="send_whatsapp_message"),
    path('webhook/', whatsapp_webhook, name="whatsapp_webhook"),
]
