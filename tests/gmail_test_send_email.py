# run from the root directory:
# python -m tests.gmail_test_send_email

from src.infrastructure.email_service import EmailService

# Configuration
SERVICE_ACCOUNT_FILE = './env/service_account_gmail-agent.json'
USER_EMAIL = 'michael@mgy.one'

# Initialize EmailService
email_service = EmailService(SERVICE_ACCOUNT_FILE, USER_EMAIL)

# Send email
to_email = 'michael801898@gmail.com'
subject = 'Hello from Service Account'
message_text = 'Test message from Gmail API'

message_id = email_service.send_email(to_email, subject, message_text)
print(f"Message ID: {message_id}")