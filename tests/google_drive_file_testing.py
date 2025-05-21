# python -m tests.google_drive_file_testing

import os
from io import BytesIO
from dotenv import load_dotenv
from src.infrastructure.google_drive_service import GoogleDriveService

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Google Drive service
service_account_file = './env/service_account_gmail-agent.json'
folder_id = os.getenv('GOOGLE_UPLOADED_TRANSACTIONS_FOLDER_ID')

drive_service = GoogleDriveService(service_account_file, folder_id)

# Read file content into BytesIO
file_path = './requirements.txt'
file_name = os.path.basename(file_path)

with open(file_path, 'rb') as f:
    file_content = BytesIO(f.read())

# Upload the file
file_id = drive_service.upload_file(file_name, file_content)

if file_id:
    print(f'File uploaded successfully!')
    print(f'File ID: {file_id}')
    
    # Get and print the file URL
    file_url = drive_service.get_file_url(file_id)
    if file_url:
        print(f'File URL: {file_url}')
else:
    print('Failed to upload file')

