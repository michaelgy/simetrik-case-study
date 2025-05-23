# python -m tests.tools.test_email_history_sheet_tools

import os
from dotenv import load_dotenv
from src.infrastructure.transaction_sheet_service import TransactionSheetService
from src.infrastructure.tools.email_history_sheet_tools import EmailHistorySheetTools, AddEmailMessageInput

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Transaction Sheet Service
service_account_file = './env/service_account_gmail-agent.json'
sheet_id = os.getenv('GOOGLE_SHEET_TRANSACTION_ID')

transaction_service = TransactionSheetService(service_account_file, sheet_id)
email_history_tools = EmailHistorySheetTools(transaction_service)

def test_read_all_email_history():
    print("\n=== Testing read_all_email_history ===")
    result = email_history_tools.tools[0].func(None)
    print(result)

def test_find_email_history():
    print("\n=== Testing find_email_history ===")
    email_id = "TEST-EMAIL-001"
    result = email_history_tools.tools[1].func(email_id)
    print(result)
    email_id = "HOg7vf-cUx27Q"
    result = email_history_tools.tools[1].func(email_id)
    print(result)

def test_add_email_message():
    print("\n=== Testing add_email_message ===")
    input_data = {
        "email_id": "HOg7vf-cUx27Q",
        "message": "Test email message from EmailHistoryTools",
    }
    input_obj = AddEmailMessageInput(**input_data)
    result = email_history_tools.tools[2].func(input_obj)
    print(result)

if __name__ == "__main__":
    # Run all tests
    test_read_all_email_history()
    test_add_email_message()
    test_find_email_history()