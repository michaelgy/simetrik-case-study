from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

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

    def _get_message_details(self, message_id):
        msg_detail = self.service.users().messages().get(userId='me', id=message_id).execute()
        payload = msg_detail.get('payload', {})
        headers = payload.get('headers', [])

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), '(No Sender)')

        body = self._extract_body(payload)

        self._mark_as_read(message_id)

        return {
            'id': message_id,
            'subject': subject,
            'from': from_email,
            'body': body
        }

    def _extract_body(self, payload):
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            body_data = payload.get('body', {}).get('data')
            if body_data:
                return base64.urlsafe_b64decode(body_data).decode('utf-8')
        return None

    def _mark_as_read(self, message_id):
        self.service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute() 