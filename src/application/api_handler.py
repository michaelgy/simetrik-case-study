from flask import Flask
from flask_cors import CORS
from src.application.wp_webhook_handler import create_webhook_blueprint
from src.application.text_chat_agent_handler import create_text_chat_agent_blueprint
from src.infrastructure.whatsapp_service import WhatsAppService
from src.infrastructure.gemini_text_agent import GeminiTextAgent

class APIHandler:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        # Initialize Services
        self.whatsapp_service = WhatsAppService()
        self.text_chat_agent = GeminiTextAgent()
        self._register_blueprints()

    def _register_blueprints(self):
        self.app.register_blueprint(create_webhook_blueprint(self.whatsapp_service))
        self.app.register_blueprint(create_text_chat_agent_blueprint(self.text_chat_agent))
        
    def run(self, host: str = '127.0.0.1', port: int = 5001):
        self.app.run(host=host, port=port)