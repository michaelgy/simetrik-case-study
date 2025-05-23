from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class AddEmailMessageInput(BaseModel):
    email_id: str = Field(..., description="EMAIL ID for the message.")
    message: str = Field(..., description="The email message content.")

class EmailHistorySheetTools:
    def __init__(self, transaction_service):
        self.transaction_service = transaction_service
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        # Tool 1: Read all email history (no input required)
        def list_all_email_history(_=None) -> str:
            """Return all email history records as a string list."""
            self.transaction_service.email_history.reload_data()
            history = self.transaction_service.email_history.read_all()
            return history.to_string()

        read_all_tool = Tool(
            name="read_all_email_history",
            func=list_all_email_history,
            description="Read all email history records from the sheet. (No input required)"
        )

        # Tool 2: Find email history by EMAIL ID
        def find_email_history_by_id(email_id: str) -> str:
            """Find and return email history records by EMAIL ID."""
            self.transaction_service.email_history.reload_data()
            result = self.transaction_service.email_history.find('EMAIL ID', email_id)
            return result.to_string() if result is not None and not result.empty else f"Email history for ID {email_id} not found."

        find_email_tool = Tool(
            name="find_email_history",
            func=find_email_history_by_id,
            description="Find email history records by EMAIL ID. Input is the EMAIL ID to look up."
        )

        # Tool 3: Add a new email message
        def add_email_message_func(input: AddEmailMessageInput) -> str:
            """Add a new email message to the history."""
            success = self.transaction_service.add_email_message(input.email_id, input.message)
            if success:
                self.transaction_service.email_history.save_changes()
            return f"Email message for ID {input.email_id} added successfully." if success else f"Failed to add email message for ID {input.email_id}."

        add_email_tool = StructuredTool.from_function(add_email_message_func)
        add_email_tool.name = "add_email_message"
        add_email_tool.description = "Add a new email message to the history. Provide email_id, message, and movement_number."

        # Collect all tools into a list
        tools = [
            read_all_tool,
            find_email_tool,
            add_email_tool,
        ]

        return tools 