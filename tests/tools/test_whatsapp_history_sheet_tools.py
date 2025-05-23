# python -m tests.tools.test_whatsapp_history_sheet_tools

import os
from dotenv import load_dotenv
from src.infrastructure.transaction_sheet_service import TransactionSheetService
from src.infrastructure.tools.whatsapp_history_sheet_tools import WhatsAppHistorySheetTools, AddWhatsAppMessageInput

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Transaction Sheet Service
service_account_file = './env/service_account_gmail-agent.json'
sheet_id = os.getenv('GOOGLE_SHEET_TRANSACTION_ID')

transaction_service = TransactionSheetService(service_account_file, sheet_id)
whatsapp_history_tools = WhatsAppHistorySheetTools(transaction_service)

def test_read_all_whatsapp_history():
    print("\n=== Testing read_all_whatsapp_history ===")
    result = whatsapp_history_tools.tools[0].func(None)
    print(result)

def test_find_whatsapp_history():
    print("\n=== Testing find_whatsapp_history ===")
    wp_id = "wp_001"  # Use an existing WhatsApp ID
    result = whatsapp_history_tools.tools[1].func(wp_id)
    print(result)
    wp_id = "0d0PcC-b8eSAX"  # Use an existing WhatsApp ID
    result = whatsapp_history_tools.tools[1].func(wp_id)
    print(result)

def test_add_whatsapp_message():
    print("\n=== Testing add_whatsapp_message ===")
    input_data = {
        "wp_id": "0d0PcC-b8eSAX",
        "message": "Test WhatsApp message from WhatsAppHistoryTools",
    }
    input_obj = AddWhatsAppMessageInput(**input_data)
    result = whatsapp_history_tools.tools[2].func(input_obj)
    print(result)

if __name__ == "__main__":
    # Run all tests
    test_read_all_whatsapp_history()
    test_add_whatsapp_message()
    test_find_whatsapp_history()