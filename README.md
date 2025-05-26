# Simetrik Case Study - Remediation Agent

A Python-based remediation agent that automates the process of handling transaction remediation requests through email and WhatsApp communications.

## Project Description

This project implements an automated remediation system that:

-   Processes transaction files in XLSX format
-   Automatically sends remediation requests via email and WhatsApp
-   Tracks communication history
-   Manages transaction states
-   Integrates with Google Services (Gmail, Drive, Sheets)
-   Provides a REST API for file processing and communication

## Prerequisites

-   Python 3.8+
-   Google Cloud Project with enabled APIs:
    -   Gmail API
    -   Google Drive API
    -   Google Sheets API
-   Service account credentials
-   WhatsApp Business API access (Wasender)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/simetrik-case-study.git
cd simetrik-case-study
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables in `env/.env`:

```env
GOOGLE_SHEET_TRANSACTION_ID=your_sheet_id
GOOGLE_UPLOADED_TRANSACTIONS_FOLDER_ID=your_folder_id
USER_EMAIL=your_email
WASENDER_API_KEY=your_wasender_key
WASENDER_PHONE_ID=your_phone_id
```

4. Place your service account credentials in `env/service_account_gmail-agent.json`

## Running the Application

### Main Application

Run the main application using one of these methods:

1. Using Python directly:

```bash
python -m src.main
```

2. Using Docker:

```bash
# Build the image
docker build -t flask-app .

# Run the container
docker run --name simetrik-remediation-agent -p 8080:8080 flask-app
```

The API will be available at `http://localhost:8080`

## Running Tests

### Email Tests

1. Read Unread Emails:

```bash
python -m tests.gmail_test_read_emails
```

2. Send Test Email:

```bash
python -m tests.gmail_test_send_email
```

### WhatsApp Tests

1. Send WhatsApp Message:

```bash
python -m tests.whatsapp_test_send_message
```

2. Process Webhook:

```bash
python -m tests.whatsapp_test_webhook
```

### Google Drive Tests

1. Upload File:

```bash
python -m tests.google_drive_test_upload
```

2. Get File URL:

```bash
python -m tests.google_drive_test_get_url
```

### Google Sheets Tests

1. Read/Write Operations:

```bash
python -m tests.google_sheets_test_operations
```

## API Endpoints

-   `POST /file_processor_api`: Process transaction files
-   `POST /webhook`: Handle WhatsApp webhooks
-   `POST /text_chat_agent_api`: Interact with the text chat agent

## Project Structure

```
simetrik-case-study/
├── src/
│   ├── application/        # API handlers and business logic
│   ├── domain/            # Domain models and types
│   ├── infrastructure/    # External service integrations
│   └── main.py           # Application entry point
├── tests/                 # Test files
├── env/                   # Environment files
└── requirements.txt       # Project dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
