from datetime import datetime
import io
from flask import Blueprint, request, jsonify
import pandas as pd
import secrets
import string

from src.infrastructure.worksheets.states_worksheet import StatesWorksheet

def generate_secure_unique_id():
    chars = string.ascii_letters + string.digits
    part1 = ''.join(secrets.choice(chars) for _ in range(6))
    part2 = ''.join(secrets.choice(chars) for _ in range(6))
    return f"{part1}-{part2}"

def default_email_message(movement_number, reference, email_id):
    return f"""Dear client, 

we inform you that the transaction N°{movement_number} with reference {reference} is pending due to missing documentation.
Please be so kind as to reply to this message by attaching a copy of your personal ID.

Best regards, Simetrik team
remediation-id@[{email_id}]
"""

def default_whatsapp_message(movement_number, reference, wp_id):
    return f"""Dear client, 

we inform you that the transaction N°{movement_number} with reference {reference}  is pending a reimbursement.
Please be so kind as to reply to this email by attaching a copy of reimbursement confirmation

Best regards, Simetrik team
remediation-id@[{wp_id}]
"""
def create_file_processor_blueprint(file_parser, transaction_service, google_drive_service, email_service, whatsapp_messages_queue):
    blueprint = Blueprint('file_processor_api', __name__)

    @blueprint.route('/file_processor_api', methods=['POST'])
    def file_processor_api():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
            # Read file content into memory
            file_stream = io.BytesIO(file.read())
            
            # Parse the uploaded file
            new_transactions_df = file_parser.read_file(file_stream, converters={'TELEFONO': str})
            
            # Get existing transactions
            transaction_service.reload_all_data()
            existing_transactions_df = transaction_service.transactions.read_all()
            
            # Remove transactions that already exist
            if not existing_transactions_df.empty:
                new_transactions_df = new_transactions_df[
                    ~new_transactions_df['N° Movimiento'].isin(existing_transactions_df['N° Movimiento'])
                ]

            if new_transactions_df.empty:
                return jsonify({"response": "No new transactions to process"})

            # Split transactions based on QUERY value
            protocol_2b_df = new_transactions_df[new_transactions_df['QUERY'] == 2].copy()
            protocol_3c_df = new_transactions_df[new_transactions_df['QUERY'] == 3].copy()
            no_procesado_df = new_transactions_df[
                ~new_transactions_df['QUERY'].isin([2, 3])
            ].copy()

            # Add state to each DataFrame
            protocol_2b_df['ESTADO DE REMEDIACION'] = StatesWorksheet.EN_PROCESO
            protocol_3c_df['ESTADO DE REMEDIACION'] = StatesWorksheet.EN_PROCESO
            no_procesado_df['ESTADO DE REMEDIACION'] = StatesWorksheet.NO_PROCESADO

            # Send emails for protocol 2b transactions
            protocol_2b_index_to_drop = []
            for index, row in protocol_2b_df.iterrows():
                if pd.notna(row.get('CORREO')):
                    movement_number = row['N° Movimiento']
                    email_id = generate_secure_unique_id()
                    subject = f"Transactions Pending Due to Missing Documents - {movement_number}"
                    message = default_email_message(movement_number, row['Referencia'], email_id)
                    try:
                        email_service.send_email(row['CORREO'], subject, message)
                        protocol_2b_df.at[index, 'EMAIL ID'] = email_id
                    except Exception as e:
                        protocol_2b_index_to_drop.append(index)
                        print(f"Error sending email to {row['CORREO']} from {email_service.user_email}: {str(e)}")

            protocol_2b_df.drop(protocol_2b_index_to_drop, inplace=True)

            # Send whatsapp messages for protocol 3c transactions
            protocol_3c_index_to_drop = []
            for index, row in protocol_3c_df.iterrows():
                if pd.notna(row.get('TELEFONO')):
                    movement_number = row['N° Movimiento']
                    cellphone = row['TELEFONO']
                    wp_id = generate_secure_unique_id()
                    message = default_whatsapp_message(movement_number, row['Referencia'], wp_id)
                    try:
                        whatsapp_messages_queue.put_message(cellphone, message, wp_id)
                        protocol_3c_df.at[index, 'WP ID'] = wp_id
                    except Exception as e:
                        protocol_3c_index_to_drop.append(index)
                        print(f"Error sending whatsapp message to {cellphone}: {str(e)}")

            protocol_3c_df.drop(protocol_3c_index_to_drop, inplace=True)

            # Add transactions to the worksheet
            for df in [protocol_2b_df, protocol_3c_df, no_procesado_df]:
                if not df.empty:
                    for _, row in df.iterrows():
                        transaction_service.transactions.add(row.to_dict())

            # Save all changes
            transaction_service.save_all_changes()

            file_name = f"{datetime.now().strftime(DATE_FORMAT)}_{file.filename}"
            file_id = google_drive_service.upload_file(file_name, file_stream)
            
            return jsonify({
                "response": "Processing completed",
                "summary": {
                    "total_new_transactions": len(new_transactions_df),
                    "protocol_2b_count": len(protocol_2b_df),
                    "protocol_2b_dropped": len(protocol_2b_index_to_drop),
                    "protocol_3c_count": len(protocol_3c_df),
                    "protocol_3c_dropped": len(protocol_3c_index_to_drop),
                    "no_procesado_count": len(no_procesado_df),
                },
                "file_id": file_id
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return blueprint