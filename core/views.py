from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import render

class MessageListView(generics.ListCreateAPIView):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class SendMessageAPI(APIView):
    def post(self, request):
        message = request.data.get("message", "")
        if not message.strip():
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "chat_chat_room",
            {
                "type": "chat.message",
                "message": message
            }
        )

        return Response({"status": "Message sent to WebSocket clients"}, status=status.HTTP_200_OK)

