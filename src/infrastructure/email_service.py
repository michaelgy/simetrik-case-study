from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import logging
from mailparser_reply import EmailReplyParser
from typing import Dict, List, Optional, Any

class EmailService:
    def __init__(self, service_account_file, user_email):
        self.service_account_file = service_account_file
        self.user_email = user_email
        self.scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/gmail.send',
            'https://www.googleapis.com/auth/gmail.modify'
        ]
        self.service = self._build_service()

    def _build_service(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file,
            scopes=self.scopes
        ).with_subject(self.user_email)
        return build('gmail', 'v1', credentials=credentials)

    def send_email(self, to, subject, message_text):
        message = self._create_message(to, subject, message_text)
        return self._send_message(message)

    def _create_message(self, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = self.user_email
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {'raw': raw}

    def _send_message(self, message):
        result = self.service.users().messages().send(userId='me', body=message).execute()
        return result['id']

    def read_unread_emails(self, max_results=3):
        response = self.service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=max_results).execute()
        messages = response.get('messages', [])
        return [self._get_message_details(msg['id']) for msg in messages]

    def _get_message_details(self, message_id: str) -> Dict[str, Any]:
        """
        Get detailed information about an email message including attachments
        Args:
            message_id: The ID of the message to retrieve
        Returns:
            Dict containing message details including subject, from, body, and attachments
        """
        try:
            msg_detail = self.service.users().messages().get(userId='me', id=message_id).execute()
            payload = msg_detail.get('payload', {})
            headers = payload.get('headers', [])

            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), '(No Sender)')

            # Extract body and attachments
            body, attachments = self._extract_body_and_attachments(payload)

            # Mark the message as read
            #self._mark_as_read(message_id)

            return {
                'id': message_id,
                'subject': subject,
                'from': from_email,
                'body': body,
                'attachments': attachments
            }
        except Exception as e:
            logging.error(f"Error getting message details: {e}")
            return {
                'id': message_id,
                'subject': '(Error)',
                'from': '(Error)',
                'body': None,
                'attachments': []
            }

    def _extract_body_and_attachments(self, payload: Dict[str, Any]) -> tuple[str, List[Dict[str, Any]]]:
        """
        Extract both body text and attachments from the email payload
        Args:
            payload: The message payload from Gmail API
        Returns:
            Tuple containing (body_text, attachments_list)
        """
        body_text = ""
        attachments = []

        def process_part(part: Dict[str, Any]):
            nonlocal body_text
            mime_type = part.get('mimeType', '')
            
            # Handle multipart messages
            if mime_type.startswith('multipart/'):
                for subpart in part.get('parts', []):
                    process_part(subpart)
                return

            # Handle attachments
            if part.get('filename'):
                attachment = {
                    'filename': part.get('filename'),
                    'mime_type': mime_type,
                    'attachment_id': part.get('body', {}).get('attachmentId'),
                    'size': part.get('body', {}).get('size', 0)
                }
                attachments.append(attachment)
                return

            # Handle body text
            if mime_type == 'text/plain':
                data = part.get('body', {}).get('data')
                if data:
                    try:
                        decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')
                        latest_reply = EmailReplyParser(languages=['en', 'es']).parse_reply(text=decoded_data)
                        body_text += latest_reply.strip() + "\n"
                    except Exception as e:
                        logging.error(f"Error decoding body text: {e}")

        # Process the payload
        process_part(payload)

        return body_text.strip(), attachments

    def _mark_as_read(self, message_id):
        self.service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

    def get_attachment(self, message_id: str, attachment_id: str) -> Optional[bytes]:
        """
        Get the content of an attachment
        Args:
            message_id: The ID of the message containing the attachment
            attachment_id: The ID of the attachment to retrieve
        Returns:
            Optional[bytes]: The attachment content if successful, None otherwise
        """
        try:
            attachment = self.service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()
            
            if attachment and 'data' in attachment:
                return base64.urlsafe_b64decode(attachment['data'])
            return None
        except Exception as e:
            logging.error(f"Error getting attachment: {e}")
            return None 