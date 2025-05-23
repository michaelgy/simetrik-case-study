# python -m tests.tools.test_email_service_tools

import os
from dotenv import load_dotenv
from src.infrastructure.email_service import EmailService
from src.infrastructure.tools.email_service_tools import EmailServiceTools, SendEmailInput

# Load environment variables
load_dotenv("./env/.env")

# Initialize the Email Service
service_account_file = './env/service_account_gmail-agent.json'
user_email = os.getenv('USER_EMAIL')

email_service = EmailService(service_account_file, user_email)
email_tools = EmailServiceTools(email_service)

def test_send_email():
    print("\n=== Testing send_email ===")
    input_data = {
        "to_email": "michael801898@gmail.com",
        "subject": "Test Email from Tools",
        "message_text": "This is a test email sent from the EmailServiceTools."
    }
    input_obj = SendEmailInput(**input_data)
    result = email_tools.tools[0].func(input_obj)
    print(result)

if __name__ == "__main__":
    # Run all tests
    test_send_email()