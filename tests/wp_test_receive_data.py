"""
This is a test script to receive data from WhatsApp Webhook
run: ngrok http --url=hamster-innocent-cicada.ngrok-free.app http://127.0.0.1:5001
the app will be available at: https://hamster-innocent-cicada.ngrok-free.app
and look at: https://dashboard.ngrok.com/endpoints
to see all endpoints
"""

from flask import Flask, request
from dotenv import load_dotenv
import os
import requests

load_dotenv("./env/.env")
app = Flask(__name__)

WASENDER_API_KEY = os.getenv("WASENDER_API_KEY")
WASENDER_PHONE_ID = os.getenv("WASENDER_PHONE_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    try:
        if data.get("event") == "chats.update":
            chats = data.get("data", {}).get("chats", {})
            messages = chats.get("messages", [])
            if messages:
                message_entry = messages[0].get("message", {})
                fromMe = message_entry.get("key", {}).get("fromMe", True)
                sender_id = message_entry.get("key", {}).get("remoteJid", "")
                message_text = message_entry.get("message", {}).get("conversation", "")
                print("Message: ", message_text, " from: ", sender_id, " fromMe: ", fromMe)
                if not fromMe and sender_id and message_text:
                    # Process the message_text as needed
                    # For example, send a response
                    sender_phone = f"+{sender_id.split("@")[0]}"
                    send_message(sender_phone, f"[ECHO] Received your message: {message_text}")
    except Exception as e:
        print(f"Error processing webhook data: {e}")
    return 'OK', 200

def send_message(to, message):
    url = "https://www.wasenderapi.com/api/send-message"
    headers = {
        "Authorization": f"Bearer {WASENDER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": to,
        "text": message
    }
    print("Sending message to: ", to, " with message: ", message, " and headers: ", headers, " and payload: ", payload)
    requests.post(url, headers=headers, json=payload)

if __name__ == '__main__':
    app.run(port=5001)