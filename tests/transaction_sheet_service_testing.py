# python -m tests.transaction_sheet_service_testing

import os
from dotenv import load_dotenv
from src.infrastructure.transaction_sheet_service import TransactionSheetService

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Transaction Sheet Service
service_account_file = './env/service_account_gmail-agent.json'
sheet_id = os.getenv('GOOGLE_SHEET_TRANSACTION_ID')

transaction_service = TransactionSheetService(service_account_file, sheet_id)

# ===== SECTION 1: TRANSACTIONS WORKSHEET OPERATIONS =====
print("\n=== TRANSACTIONS WORKSHEET OPERATIONS ===")

# Example data for transactions
transactions_data = [
    {
        'Fecha': '01-01-2023',
        'Concepto': 'Pago Servicio',
        'N° Movimiento': 1001,
        'Referencia': 'REF001',
        'Monto': 15000.0,
        'QUERY': 'Q1',
        'CORREO': 'usuario1@correo.com',
        'TELEFONO': '3001234567',
        'REMITENTE': 'Banco A',
        'ESTADO DE REMEDIACION': 'Pendiente',
        'EMAIL ID': 'email_001',
        'WP ID': 'wp_001',
        'ARCHIVO': 'archivo1.pdf'
    },
    {
        'Fecha': '02-01-2023',
        'Concepto': 'Transferencia',
        'N° Movimiento': 1002,
        'Referencia': 'REF002',
        'Monto': 25000.0,
        'QUERY': 'Q2',
        'CORREO': 'usuario2@correo.com',
        'TELEFONO': '3002345678',
        'REMITENTE': 'Banco B',
        'ESTADO DE REMEDIACION': 'Completado',
        'EMAIL ID': 'email_002',
        'WP ID': 'wp_002',
        'ARCHIVO': 'archivo2.pdf'
    },
    {
        'Fecha': '03-01-2023',
        'Concepto': 'Compra en Línea',
        'N° Movimiento': 1003,
        'Referencia': 'REF003',
        'Monto': 35000.0,
        'QUERY': 'Q3',
        'CORREO': 'usuario3@correo.com',
        'TELEFONO': '3003456789',
        'REMITENTE': 'Banco C',
        'ESTADO DE REMEDIACION': 'En Proceso',
        'EMAIL ID': 'email_003',
        'WP ID': 'wp_003',
        'ARCHIVO': 'archivo3.pdf'
    }
]

# Add transactions
print("\nAdding transactions:")
for transaction in transactions_data:
    if transaction_service.transactions.add(transaction):
        print(f"Added transaction with N° Movimiento: {transaction['N° Movimiento']}")
    else:
        print(f"Failed to add transaction with N° Movimiento: {transaction['N° Movimiento']}")

# Find a specific transaction
print("\nFinding transaction:")
movement_number = 1002
found_transaction = transaction_service.transactions.find('N° Movimiento', movement_number)
if found_transaction is not None and not found_transaction.empty:
    print(f"Found transaction with N° Movimiento {movement_number}:")
    print(found_transaction)
else:
    print(f"No transaction found with N° Movimiento {movement_number}")

# Update transaction state
print("\nUpdating transaction state:")
new_state = "Actualizado"
if transaction_service.transactions.update_state(movement_number, new_state):
    print(f"Updated state of transaction {movement_number} to '{new_state}'")
else:
    print(f"Failed to update state of transaction {movement_number}")

# ===== SECTION 2: EMAIL HISTORY OPERATIONS =====
print("\n=== EMAIL HISTORY OPERATIONS ===")

# Add email messages
print("\nAdding email messages:")
email_messages = [
    ("email_001", "Email de notificación enviado al usuario"),
    ("email_002", "Recordatorio de pago enviado"),
    ("email_003", "Confirmación de transacción enviada")
]

for email_id, message in email_messages:
    if transaction_service.add_email_message(email_id, message):
        print(f"Added email message for EMAIL ID: {email_id}")
    else:
        print(f"Failed to add email message for EMAIL ID: {email_id}")

# Find email records
print("\nFinding email records:")
email_id = "email_002"
found_emails = transaction_service.email_history.find('EMAIL ID', email_id)
if found_emails is not None and not found_emails.empty:
    print(f"Found email records for EMAIL ID {email_id}:")
    print(found_emails)
else:
    print(f"No email records found for EMAIL ID {email_id}")

# ===== SECTION 3: WHATSAPP HISTORY OPERATIONS =====
print("\n=== WHATSAPP HISTORY OPERATIONS ===")

# Add WhatsApp messages
print("\nAdding WhatsApp messages:")
whatsapp_messages = [
    ("wp_001", "Mensaje de WhatsApp enviado al usuario"),
    ("wp_002", "Recordatorio de pago por WhatsApp"),
    ("wp_003", "Confirmación de transacción por WhatsApp")
]

for wp_id, message in whatsapp_messages:
    if transaction_service.add_whatsapp_message(wp_id, message):
        print(f"Added WhatsApp message for WP ID: {wp_id}")
    else:
        print(f"Failed to add WhatsApp message for WP ID: {wp_id}")

# Find WhatsApp records
print("\nFinding WhatsApp records:")
wp_id = "wp_003"
found_whatsapp = transaction_service.whatsapp_history.find('WP ID', wp_id)
if found_whatsapp is not None and not found_whatsapp.empty:
    print(f"Found WhatsApp records for WP ID {wp_id}:")
    print(found_whatsapp)
else:
    print(f"No WhatsApp records found for WP ID {wp_id}")

# ===== SECTION 4: READ ALL DATA =====
print("\n=== READING ALL DATA ===")

# Read all transactions
print("\nAll transactions:")
all_transactions = transaction_service.transactions.read_all()
print(all_transactions)

# Read all email history
print("\nAll email history:")
all_emails = transaction_service.email_history.read_all()
print(all_emails)

# Read all WhatsApp history
print("\nAll WhatsApp history:")
all_whatsapp = transaction_service.whatsapp_history.read_all()
print(all_whatsapp)

# ===== SECTION 5: SAVE ALL CHANGES =====
print("\n=== SAVING ALL CHANGES ===")

# Save all changes
if transaction_service.save_all_changes():
    print("Successfully saved all changes to all worksheets")
else:
    print("Failed to save changes to worksheets")

# ===== SECTION 6: RELOAD DATA =====
print("\n=== RELOADING DATA ===")

# Reload all data
if transaction_service.reload_all_data():
    print("Successfully reloaded all data from worksheets")
else:
    print("Failed to reload data from worksheets") 