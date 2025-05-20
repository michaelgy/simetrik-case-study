import os
from dotenv import load_dotenv
from src.application.wp_webhook_handler import WPWebhookHandler

def main():
    # Load environment variables
    load_dotenv("./env/.env")
    
    # Create and run webhook handler
    webhook = WPWebhookHandler()
    print("Starting WhatsApp webhook server...")
    print("Server running at: http://127.0.0.1:5001")
    print("Use ngrok to expose the webhook: ngrok http 5001")
    webhook.run()

if __name__ == "__main__":
    main() 