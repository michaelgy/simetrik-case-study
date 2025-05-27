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
    
    results = []
    for email in unread_emails:
        result = "\n"
        
        result += "=" * 80 + "\n"
        result += f"From: {email['from']}" + "\n"
        result += f"Subject: {email['subject']}" + "\n"
        result += f"Message ID: {email['id']}" + "\n"
        
        # Display body
        if email['body']:
            result += "\nBody:" + "\n"
            result += "-" * 40 + "\n"
            result += email['body'] + "\n"
            result += "-" * 40 + "\n"
        else:
            result += "\n[No text body found]" + "\n"
            
        # Display attachments
        if email['attachments']:
            result += "\nAttachments:" + "\n"
            for attachment in email['attachments']:
                result += f"- {attachment['filename']}" + "\n"
                result += f"  Type: {attachment['mime_type']}" + "\n"
                result += f"  Size: {format_size(attachment['size'])}" + "\n"
                
                # Download and show first few bytes of each attachment
                content = email_service.get_attachment(email['id'], attachment['attachment_id'])
                if content:
                    preview = content[:100] if len(content) > 100 else content
                    result += f"  Preview: {preview}" + "\n"
                result += ""
        else:
            result += "\n[No attachments found]" + "\n"
        
        result += "=" * 80 + "\n"
        results.append(result)
    logging.info("\n".join(results))

if __name__ == "__main__":
    main()