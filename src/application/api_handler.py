# Libraries
import os
from flask import Flask
from flask_cors import CORS
import logging

# Infrastructure
from src.infrastructure.google_drive_service import GoogleDriveService
from src.infrastructure.google_sheets_service import GoogleSheetsService
from src.infrastructure.transaction_sheet_service import TransactionSheetService
from src.infrastructure.whatsapp_service import WhatsAppService
from src.infrastructure.gemini_text_agent import GeminiTextAgent
from src.infrastructure.xlsx_parser import XLSXParser
from src.infrastructure.email_service import EmailService
from src.infrastructure.whatsapp_service import WhatsAppService
from src.infrastructure.whatsapp_messages_queue import WhatsappMessagesQueue
from src.infrastructure.tools.transaction_sheet_tools import TransactionSheetTools

# Application
from src.application.file_processor_handler import create_file_processor_blueprint
from src.application.wp_webhook_handler import create_webhook_blueprint
from src.application.text_chat_agent_handler import create_text_chat_agent_blueprint

class APIHandler:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.logger.setLevel(logging.INFO)
        
        CORS(self.app)

        # constans
        sheet_id = os.getenv('GOOGLE_SHEET_TRANSACTION_ID')
        folder_uploaded_transactions_id = os.getenv('GOOGLE_UPLOADED_TRANSACTIONS_FOLDER_ID')
        service_account_file = './env/service_account_gmail-agent.json'
        user_email = os.getenv('USER_EMAIL') 

        # Initialize Services
        self.whatsapp_service = WhatsAppService()
        self.file_parser = XLSXParser()
        self.transaction_sheet_service = TransactionSheetService(service_account_file, sheet_id)
        self.google_drive_service = GoogleDriveService(service_account_file, folder_uploaded_transactions_id)
        self.email_service = EmailService(service_account_file, user_email)
        self.whatsapp_service = WhatsAppService()
        self.whatsapp_messages_queue = WhatsappMessagesQueue(self.whatsapp_service)

        # Initialize Tools
        self.transaction_sheet_tools = TransactionSheetTools(self.transaction_sheet_service)

        # Initialize Agents
        self.text_chat_agent = GeminiTextAgent(self.transaction_sheet_tools.tools)

        self._register_blueprints()

    def _register_blueprints(self):
        self.app.register_blueprint(create_webhook_blueprint(self.whatsapp_service))
        self.app.register_blueprint(create_text_chat_agent_blueprint(self.text_chat_agent))
        self.app.register_blueprint(create_file_processor_blueprint(
            self.file_parser, 
            self.transaction_sheet_service, 
            self.google_drive_service,
            self.email_service,
            self.whatsapp_messages_queue
        ))
    
    def run(self, host: str = "0.0.0.0", port: int = 8080):
        self.app.logger.info("Starting Api Handler server...")
        self.app.logger.info(f"Server running at: http://{host}:{port}")
        self.app.logger.info(f"Use ngrok to expose the api: ngrok http --url=hamster-innocent-cicada.ngrok-free.app http://{host}:{port}")

        self.app.logger.info("### Available endpoints:")
        for rule in self.app.url_map.iter_rules():
            self.app.logger.info(f"- {rule.endpoint:60s} {','.join(rule.methods):20s} {rule}")
        
        self.app.run(host=host, port=port)