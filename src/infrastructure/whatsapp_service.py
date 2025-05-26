import os
import requests
from typing import Optional
import logging

class WhatsAppService:
    def __init__(self):
        self.api_key = os.getenv("WASENDER_API_KEY")
        self.phone_id = os.getenv("WASENDER_PHONE_ID")
            
        self.base_url = "https://www.wasenderapi.com/api"

    def send_message(self, to: str, message: str) -> bool:
        """
        Send a message to a WhatsApp number
        Args:
            to: The recipient's phone number with country code (e.g., +1234567890)
            message: The message text to send
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        if not self.api_key:
            return False
            
        url = f"{self.base_url}/send-message"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": to,
            "text": message
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Error sending WhatsApp message: {e}")
            return False

    def process_incoming_message(self, webhook_data: dict) -> Optional[tuple]:
        """
        Process incoming webhook data from WhatsApp
        Args:
            webhook_data: The webhook data received from WhatsApp
        Returns:
            Optional[tuple]: Tuple of (sender_id, message_text) if valid message, None otherwise
        """
        try:
            if webhook_data.get("event") == "chats.update":
                chats = webhook_data.get("data", {}).get("chats", {})
                messages = chats.get("messages", [])
                if messages:
                    message_entry = messages[0].get("message", {})
                    from_me = message_entry.get("key", {}).get("fromMe", True)
                    sender_id = message_entry.get("key", {}).get("remoteJid", "")
                    message_text = message_entry.get("message", {}).get("conversation", "")
                    
                    if not from_me and sender_id and message_text:
                        return sender_id, message_text
        except Exception as e:
            logging.error(f"Error processing webhook data: {e}")
        return None 