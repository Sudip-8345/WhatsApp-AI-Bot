from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from config import Config
from bot.groq_client import GroqClient

class WhatsAppHandler:
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.groq_client = GroqClient()
        self.conversations = {}
    
    def process_incoming_message(self, message_body: str, sender_number: str) -> str:
        """Process incoming message using Groq Llama model"""
        # Get or create conversation context
        if sender_number not in self.conversations:
            self.conversations[sender_number] = []
        
        # Add user message to context
        self.conversations[sender_number].append(f"User: {message_body}")
        
        # Keep only last 5 messages for context (to avoid token limits)
        if len(self.conversations[sender_number]) > 10:
            self.conversations[sender_number] = self.conversations[sender_number][-10:]
        
        # Build context from conversation history
        context = "\n".join(self.conversations[sender_number])
        
        # Generate response using Groq
        response = self.groq_client.generate_response(message_body, context)
        
        # Add assistant response to context
        self.conversations[sender_number].append(f"Assistant: {response}")
        
        return response
    
    def send_message(self, to_number: str, message_body: str):
        message = self.client.messages.create(
            body=message_body,
            from_=Config.TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        return message.sid
    
    def clear_context(self, sender_number: str):
        if sender_number in self.conversations:
            del self.conversations[sender_number]