# run from the root directory:
# python -m tests.gmail_test_read_emails

import logging
from src.infrastructure.email_service import EmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configuration
SERVICE_ACCOUNT_FILE = './env/service_account_gmail-agent.json'
USER_EMAIL = 'michael@mgy.one'

def format_size(size_bytes):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def main():
    # Initialize EmailService
    email_service = EmailService(SERVICE_ACCOUNT_FILE, USER_EMAIL)

    # Read unread emails
    unread_emails = email_service.read_unread_emails(max_results=3)

    logging.info(f"Found {len(unread_emails)} unread messages\n")

    for email in unread_emails:
        logging.info("=" * 80)
        logging.info(f"From: {email['from']}")
        logging.info(f"Subject: {email['subject']}")
        logging.info(f"Message ID: {email['id']}")
        
        # Display body
        if email['body']:
            logging.info("\nBody:")
            logging.info("-" * 40)
            logging.info(email['body'])
            logging.info("-" * 40)
        else:
            logging.info("\n[No text body found]")

        # Display attachments
        if email['attachments']:
            logging.info("\nAttachments:")
            for attachment in email['attachments']:
                logging.info(f"- {attachment['filename']}")
                logging.info(f"  Type: {attachment['mime_type']}")
                logging.info(f"  Size: {format_size(attachment['size'])}")
                
                # Download and show first few bytes of each attachment
                content = email_service.get_attachment(email['id'], attachment['attachment_id'])
                if content:
                    preview = content[:100] if len(content) > 100 else content
                    logging.info(f"  Preview: {preview}")
                logging.info("")
        else:
            logging.info("\n[No attachments found]")
        
        logging.info("=" * 80 + "\n")

if __name__ == "__main__":
    main()