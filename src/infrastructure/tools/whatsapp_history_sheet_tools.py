from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class AddWhatsAppMessageInput(BaseModel):
    wp_id: str = Field(..., description="WP ID for the message.")
    message: str = Field(..., description="The WhatsApp message content.")

class WhatsAppHistorySheetTools:
    def __init__(self, transaction_service):
        self.transaction_service = transaction_service
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        # Tool 1: Read all WhatsApp history (no input required)
        def list_all_whatsapp_history(_=None) -> str:
            """Return all WhatsApp history records as a string list."""
            self.transaction_service.whatsapp_history.reload_data()
            history = self.transaction_service.whatsapp_history.read_all()
            return history.to_string()

        read_all_tool = Tool(
            name="read_all_whatsapp_history",
            func=list_all_whatsapp_history,
            description="Read all WhatsApp history records from the sheet. (No input required)"
        )

        # Tool 2: Find WhatsApp history by WP ID
        def find_whatsapp_history_by_id(wp_id: str) -> str:
            """Find and return WhatsApp history records by WP ID."""
            self.transaction_service.whatsapp_history.reload_data()
            result = self.transaction_service.whatsapp_history.find('WP ID', wp_id)
            return result.to_string() if result is not None and not result.empty else f"WhatsApp history for ID {wp_id} not found."

        find_whatsapp_tool = Tool(
            name="find_whatsapp_history",
            func=find_whatsapp_history_by_id,
            description="Find WhatsApp history records by WP ID. Input is the WP ID to look up."
        )

        # Tool 3: Add a new WhatsApp message
        def add_whatsapp_message_func(input: AddWhatsAppMessageInput) -> str:
            """Add a new WhatsApp message to the history."""
            success = self.transaction_service.add_whatsapp_message(input.wp_id, input.message)
            if success:
                self.transaction_service.whatsapp_history.save_changes()
            return f"WhatsApp message for ID {input.wp_id} added successfully." if success else f"Failed to add WhatsApp message for ID {input.wp_id}."

        add_whatsapp_tool = StructuredTool.from_function(add_whatsapp_message_func)
        add_whatsapp_tool.name = "add_whatsapp_message"
        add_whatsapp_tool.description = "Add a new WhatsApp message to the history. Provide wp_id, message, and movement_number."

        # Collect all tools into a list
        tools = [
            read_all_tool,
            find_whatsapp_tool,
            add_whatsapp_tool,
        ]

        return tools 