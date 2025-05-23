# python -m tests.tools.test_transaction_sheet_tools

import os
from dotenv import load_dotenv
from src.infrastructure.transaction_sheet_service import TransactionSheetService
from src.infrastructure.tools.transaction_sheet_tools import TransactionSheetTools, AddTransactionInput, UpdateTransactionInput, UpdateStateInput

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Transaction Sheet Service
service_account_file = './env/service_account_gmail-agent.json'
sheet_id = os.getenv('GOOGLE_SHEET_TRANSACTION_ID')

transaction_service = TransactionSheetService(service_account_file, sheet_id)
transaction_tools = TransactionSheetTools(transaction_service)

def test_read_all_transactions():
    print("\n=== Testing read_all_transactions ===")
    result = transaction_tools.tools[0].func(None)
    print(result)

def test_find_transaction():
    print("\n=== Testing find_transaction ===")
    movement_number = "9999"  # Use an existing transaction number
    result = transaction_tools.tools[1].func(movement_number)
    print(result)

def test_add_transaction():
    print("\n=== Testing add_transaction ===")
    input_data = {
        "date": "01-01-2024",
        "concept": "Test Transaction",
        "movement_number": "9999",
        "reference": "TEST001",
        "amount": 1000.0,
        "query": "Q1",
        "email": "michael801898@gmail.com",
        "cellphone": "+573135432343",
        "sender": "Test Bank",
        "state": "No Procesado",
        "email_id": "",
        "wp_id": "",
        "file_path": "test.pdf"
    }
    input_obj = AddTransactionInput(**input_data)
    result = transaction_tools.tools[2].func(input_obj)
    print(result)

def test_update_transaction():
    print("\n=== Testing update_transaction ===")
    input_data = {
        "column_to_search": "N° Movimiento",
        "value_to_search": "9999",
        "concept": "Updated Test Transaction",
        "amount": 2000.0,
        "state": "En Proceso"
    }
    input_obj = UpdateTransactionInput(**input_data)
    result = transaction_tools.tools[3].func(input_obj)
    print(result)

def test_update_transaction_status():
    print("\n=== Testing update_transaction_status ===")
    input_data = {
        "movement_number": "9999",
        "new_status": "Completado"
    }
    input_obj = UpdateStateInput(**input_data)
    result = transaction_tools.tools[4].func(input_obj)
    print(result)

if __name__ == "__main__":
    # Run all tests
    test_read_all_transactions()
    test_add_transaction()
    test_find_transaction()
    test_update_transaction()
    test_update_transaction_status()