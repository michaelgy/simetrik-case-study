from langchain.agents import Tool
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class QueueMessageInput(BaseModel):
    cellphone: str = Field(..., description="Recipient's phone number.")
    message: str = Field(..., description="WhatsApp message content.")
    wp_id: str = Field(..., description="Unique identifier for the message.")

class WhatsAppMessagesQueueTools:
    def __init__(self, whatsapp_messages_queue):
        self.whatsapp_messages_queue = whatsapp_messages_queue
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        # Tool 1: Queue a WhatsApp message
        def queue_message_func(input: QueueMessageInput) -> str:
            """Queue a WhatsApp message for sending."""
            try:
                self.whatsapp_messages_queue.put_message(input.cellphone, input.message, input.wp_id)
                return f"Message queued successfully for {input.cellphone} with ID {input.wp_id}"
            except Exception as e:
                return f"Failed to queue message: {str(e)}"

        queue_message_tool = StructuredTool.from_function(queue_message_func)
        queue_message_tool.name = "queue_whatsapp_message"
        queue_message_tool.description = "Queue a WhatsApp message for sending. Provide cellphone, message, and wp_id."

        # Collect all tools into a list
        tools = [
            queue_message_tool
        ]

        return tools 