from flask import Flask, request
from src.infrastructure.whatsapp_service import WhatsAppService

class WPWebhookHandler:
    def __init__(self):
        self.app = Flask(__name__)
        self.whatsapp_service = WhatsAppService()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/webhook', methods=['POST'])
        def webhook():
            data = request.get_json()
            result = self.whatsapp_service.process_incoming_message(data)
            
            if result:
                sender_id, message_text = result
                sender_phone = f"+{sender_id.split('@')[0]}"
                self.whatsapp_service.send_message(
                    sender_phone,
                    f"[ECHO] Received your message: {message_text}"
                )
            
            return 'OK', 200

    def run(self, host: str = '127.0.0.1', port: int = 5001):
        """
        Run the Flask application
        Args:
            host: The host to run the server on
            port: The port to run the server on
        """
        self.app.run(host=host, port=port) 