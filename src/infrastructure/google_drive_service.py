import os
from typing import Optional
from io import BytesIO
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import logging

class GoogleDriveService:
    def __init__(self, service_account_file: str, folder_id: str):
        """
        Initialize the Google Drive Service
        Args:
            service_account_file: Path to the service account JSON file
            folder_id: ID of the Google Drive folder to upload files to
        """
        self.service_account_file = service_account_file
        self.folder_id = folder_id
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.service = self._build_service()

    def _build_service(self):
        """
        Build and return the Google Drive API service
        Returns:
            The Google Drive API service instance
        """
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, 
            scopes=self.scopes
        )
        return build('drive', 'v3', credentials=credentials)

    def upload_file(self, file_name: str, file_content: BytesIO) -> Optional[str]:
        """
        Upload a file to Google Drive
        Args:
            file_name: Name of the file to be uploaded
            file_content: BytesIO object containing the file content
        Returns:
            Optional[str]: The ID of the uploaded file if successful, None otherwise
        """
        try:
            # File metadata
            file_metadata = {
                'name': file_name,
                'parents': [self.folder_id]
            }

            # Create media content from BytesIO
            media = MediaIoBaseUpload(
                file_content,
                mimetype='application/octet-stream',
                resumable=True
            )

            # Upload the file
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            return file.get('id')
        except Exception as e:
            logging.error(f"Error uploading file to Google Drive: {e}")
            return None

    def get_file_url(self, file_id: str) -> Optional[str]:
        """
        Get the web view URL for a file
        Args:
            file_id: The ID of the file in Google Drive
        Returns:
            Optional[str]: The web view URL if successful, None otherwise
        """
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='webViewLink'
            ).execute()
            return file.get('webViewLink')
        except Exception as e:
            logging.error(f"Error getting file URL: {e}")
            return None 