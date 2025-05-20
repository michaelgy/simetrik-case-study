# run from the root directory:
# python -m tests.gmail_test_read_emails

from src.infrastructure.email_service import EmailService

# Configuration
SERVICE_ACCOUNT_FILE = './env/service_account_gmail-agent.json'
USER_EMAIL = 'michael@mgy.one'

# Initialize EmailService
email_service = EmailService(SERVICE_ACCOUNT_FILE, USER_EMAIL)

# Read unread emails
unread_emails = email_service.read_unread_emails(max_results=3)

print(f"Found {len(unread_emails)} unread messages\n")

for email in unread_emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print("Body:", email['body'][:200] if email['body'] else "[No text found]", "\n")