from flask import Flask, request, jsonify, render_template
from twilio.twiml.messaging_response import MessagingResponse
from bot.handlers import WhatsAppHandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
whatsapp_handler = WhatsAppHandler()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    print("Webhook called!")
    print("Form data:", dict(request.form))
    
    try:
        incoming_message = request.form.get('Body', '').strip()
        sender_number = request.form.get('From', '').replace('whatsapp:', '')
        
        print(f"Message: {incoming_message}, From: {sender_number}")
        
        if not incoming_message or not sender_number:
            print("No message or sender number found")
            response = MessagingResponse()
            return str(response)
        
        # Process message and generate response
        response_text = whatsapp_handler.process_incoming_message(incoming_message, sender_number)
        print(f"Generated response: {response_text}")
        
        # Create TwiML response
        twiml_response = MessagingResponse()
        twiml_response.message(response_text)
        
        return str(twiml_response)
    
    except Exception as e:
        print(f"Error processing message: {e}")
        twiml_response = MessagingResponse()
        twiml_response.message("Sorry, I encountered an error. Please try again later.")
        return str(twiml_response)

@app.route('/send-message', methods=['POST'])
def send_message():
    """Endpoint to send proactive messages"""
    try:
        data = request.json
        to_number = data.get('to')
        message_body = data.get('message')
        
        if not to_number or not message_body:
            return jsonify({'error': 'Missing parameters'}), 400
        
        message_sid = whatsapp_handler.send_message(to_number, message_body)
        return jsonify({'success': True, 'message_sid': message_sid})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)