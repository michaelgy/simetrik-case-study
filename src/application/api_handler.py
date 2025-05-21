from flask import Flask
from src.application.wp_webhook_handler import create_webhook_blueprint
from src.infrastructure.whatsapp_service import WhatsAppService

class APIHandler:
    def __init__(self):
        self.app = Flask(__name__)
        
        # Initialize Services
        self.whatsapp_service = WhatsAppService()

        
        self._register_blueprints()

    def _register_blueprints(self):
        self.app.register_blueprint(create_webhook_blueprint(self.whatsapp_service))

    def run(self, host: str = '127.0.0.1', port: int = 5001):
        self.app.run(host=host, port=port)