# python -m tests.google_sheets_read_write_testing

import os
from dotenv import load_dotenv
from src.infrastructure.google_sheets_service import GoogleSheetsService

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Google Sheets service
service_account_file = './env/service_account_gmail-agent.json'
sheet_id = os.getenv('GOOGLE_SHEET_TRANSACTION_ID')
worksheet_name = 'Transacciones'

sheets_service = GoogleSheetsService(service_account_file, sheet_id, worksheet_name)

# Example data to add
new_rows = [
    {
        'Fecha': '2023-01-01',
        'Concepto': 'Pago Servicio',
        'N° Movimiento': 1001,
        'Referencia': 'REF001',
        'Monto': 15000.0,
        'QUERY': 'Q1',
        'CORREO': 'usuario1@correo.com',
        'TELEFONO': '3001234567',
        'REMITENTE': 'Banco A',
        'ESTADO DE REMEDIACION': 'Pendiente'
    },
    {
        'Fecha': '2023-01-02',
        'Concepto': 'Transferencia',
        'N° Movimiento': 1002,
        'Referencia': 'REF002',
        'Monto': 25000.0,
        'QUERY': 'Q2',
        'CORREO': 'usuario2@correo.com',
        'TELEFONO': '3002345678',
        'REMITENTE': 'Banco B',
        'ESTADO DE REMEDIACION': 'Completado'
    },
    {
        'Fecha': '2023-01-03',
        'Concepto': 'Compra en Línea',
        'N° Movimiento': 1003,
        'Referencia': 'REF003',
        'Monto': 35000.0,
        'QUERY': 'Q3',
        'CORREO': 'usuario3@correo.com',
        'TELEFONO': '3003456789',
        'REMITENTE': 'Banco C',
        'ESTADO DE REMEDIACION': 'En Proceso'
    }
]

# Add rows to in-memory DataFrame
for row in new_rows:
    if sheets_service.add_row(row):
        print(f"Added row with N° Movimiento: {row['N° Movimiento']}")
    else:
        print(f"Failed to add row with N° Movimiento: {row['N° Movimiento']}")

# Find a specific row
movement_number = 1002
found_rows = sheets_service.find_row('N° Movimiento', movement_number)
if found_rows is not None:
    print(f"\nFound rows with N° Movimiento {movement_number}:")
    print(found_rows)
else:
    print(f"\nNo rows found with N° Movimiento {movement_number}")

# Update a row in the in-memory DataFrame
update_data = {
    'ESTADO DE REMEDIACION': 'Actualizado',
    'Monto': 30000.0
}
if sheets_service.update_row('N° Movimiento', movement_number, update_data):
    print(f"\nUpdated row with N° Movimiento {movement_number}")
else:
    print(f"\nFailed to update row with N° Movimiento {movement_number}")

# Read all data from in-memory DataFrame
all_data = sheets_service.read_all_data()
print("\nAll data in memory:")
print(all_data)

# Save all changes to the worksheet
if sheets_service.save_changes():
    print("\nSuccessfully saved all changes to the worksheet")
else:
    print("\nFailed to save changes to the worksheet")
