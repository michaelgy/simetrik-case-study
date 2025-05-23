# python -m tests.tools.test_states_sheet_tools

import os
from dotenv import load_dotenv
from src.infrastructure.transaction_sheet_service import TransactionSheetService
from src.infrastructure.tools.states_sheet_tools import StatesSheetTools

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Transaction Sheet Service
service_account_file = './env/service_account_gmail-agent.json'
sheet_id = os.getenv('GOOGLE_SHEET_TRANSACTION_ID')

transaction_service = TransactionSheetService(service_account_file, sheet_id)
states_tools = StatesSheetTools(transaction_service)

def test_read_all_states():
    print("\n=== Testing read_all_states ===")
    result = states_tools.tools[0].func(None)
    print(result)

def test_find_state():
    print("\n=== Testing find_state ===")
    state_name = "No Procesado"  # Use an existing state
    result = states_tools.tools[1].func(state_name)
    print(result)
    state_name = "Hello"  # Use an existing state
    result = states_tools.tools[1].func(state_name)
    print(result)

if __name__ == "__main__":
    # Run all tests
    test_read_all_states()
    test_find_state()