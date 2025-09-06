import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        secret_key = secrets.token_hex(32)
        print(f"Generated SECRET_KEY: {secret_key}")
    
    SECRET_KEY = secret_key