from groq import Groq
from config import Config
from datetime import datetime

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = "llama-3.1-8b-instant"
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using Groq's Llama model with custom prompt"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
        
            SYSTEM_PROMPT = f"""
            Today is {today}.
            You are a helpful WhatsApp assistant. Be friendly and concise.
            Keep responses brief (1-2 sentences max) for mobile messaging.
            Answer helpfully or ask clarifying questions if needed.
            """
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
            ]
            
            # Add conversation history
            if context:
                messages.append({"role": "user", "content": context})
            
            # Add current message
            messages.append({"role": "user", "content": prompt})
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.7,
                max_tokens=500  
            )
            
            return chat_completion.choices[0].message.content.strip()
    
        except Exception as e:
            print(f"Error generating response from Groq: {e}")
            return "I'm experiencing technical difficulties. Please try again later."