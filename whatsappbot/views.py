from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Twilio client setup
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@api_view(["POST"])
def send_whatsapp_message(request):
    """Send a WhatsApp message using Twilio API"""
    to_number = request.data.get("to")
    message_body = request.data.get("message")

    if not to_number or not message_body:
        return Response({"error": "Missing 'to' or 'message' field"}, status=400)

    try:
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f"whatsapp:{to_number}"
        )
        return Response({"message_sid": message.sid, "status": "Message sent successfully"})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["POST"])
def whatsapp_webhook(request):
    """Handle incoming WhatsApp messages"""
    incoming_msg = request.data.get("Body", "").strip().lower()
    sender = request.data.get("From")

    response = MessagingResponse()
    reply = response.message()

    if "hello" in incoming_msg:
        reply.body("Hello! How can I assist you today?")
    elif "help" in incoming_msg:
        reply.body("You can ask me about your orders, account details, or general queries.")
    else:
        reply.body("Sorry, I didn't understand that. Type 'help' for options.")

    return Response(str(response), content_type="text/xml")
