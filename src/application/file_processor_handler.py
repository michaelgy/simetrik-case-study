from datetime import datetime
import io
from flask import Blueprint, request, jsonify
import pandas as pd

from src.infrastructure.worksheets.states_worksheet import StatesWorksheet

def create_file_processor_blueprint(file_parser, transaction_service, google_drive_service):
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
            new_transactions_df = file_parser.read_file(file_stream)
            
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
                    "protocol_3c_count": len(protocol_3c_df),
                    "no_procesado_count": len(no_procesado_df)
                },
                "file_id": file_id
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return blueprint