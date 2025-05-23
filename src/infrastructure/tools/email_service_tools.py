from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class SendEmailInput(BaseModel):
    to_email: str = Field(..., description="Recipient's email address.")
    subject: str = Field(..., description="Email subject.")
    message_text: str = Field(..., description="Email message content.")

class EmailServiceTools:
    def __init__(self, email_service):
        self.email_service = email_service
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        # Tool 1: Send an email
        def send_email_func(input: SendEmailInput) -> str:
            """Send an email using the email service."""
            try:
                message_id = self.email_service.send_email(input.to_email, input.subject, input.message_text)
                return f"Email sent successfully. Message ID: {message_id}"
            except Exception as e:
                return f"Failed to send email: {str(e)}"

        send_email_tool = StructuredTool.from_function(send_email_func)
        send_email_tool.name = "send_email"
        send_email_tool.description = "Send an email. Provide to_email, subject, and message_text."

        # Collect all tools into a list
        tools = [
            send_email_tool
        ]

        return tools 