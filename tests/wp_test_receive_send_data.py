# run from the root directory:
# python -m tests.wp_test_receive_send_data

"""
This is a test script to receive data from WhatsApp Webhook
run: ngrok http --url=hamster-innocent-cicada.ngrok-free.app http://127.0.0.1:5001
the app will be available at: https://hamster-innocent-cicada.ngrok-free.app
and look at: https://dashboard.ngrok.com/endpoints
to see all endpoints
"""

from flask import Flask, request
from dotenv import load_dotenv
from src.infrastructure.whatsapp_service import WhatsAppService

load_dotenv("./env/.env")
app = Flask(__name__)

# Initialize WhatsApp service
whatsapp_service = WhatsAppService()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    result = whatsapp_service.process_incoming_message(data)
    
    if result:
        sender_id, message_text = result
        sender_phone = f"+{sender_id.split('@')[0]}"
        whatsapp_service.send_message(
            sender_phone,
            f"[ECHO] Received your message: {message_text}"
        )
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5001)