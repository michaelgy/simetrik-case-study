# python -m tests.tools.test_whatsapp_messages_queue_tools

from dotenv import load_dotenv
from src.infrastructure.whatsapp_service import WhatsAppService
from src.infrastructure.whatsapp_messages_queue import WhatsappMessagesQueue
from src.infrastructure.tools.whatsapp_messages_queue_tools import WhatsAppMessagesQueueTools, QueueMessageInput

# Load environment variables
load_dotenv("./env/.env")

# Initialize the WhatsApp Services
whatsapp_service = WhatsAppService()
whatsapp_messages_queue = WhatsappMessagesQueue(whatsapp_service)
whatsapp_tools = WhatsAppMessagesQueueTools(whatsapp_messages_queue)

def test_queue_message():
    print("\n=== Testing queue_whatsapp_message ===")
    input_data = {
        "cellphone": "+573135432343",
        "message": "Test message from WhatsAppMessagesQueueTools",
        "wp_id": "TEST-WP-001"
    }
    input_obj = QueueMessageInput(**input_data)
    result = whatsapp_tools.tools[0].func(input_obj)
    print(result)
    
    input_data = {
        "cellphone": "+573135432343",
        "message": "Test 2 message from WhatsAppMessagesQueueTools",
        "wp_id": "TEST-WP-002"
    }
    input_obj = QueueMessageInput(**input_data)
    result = whatsapp_tools.tools[0].func(input_obj)
    print(result)

if __name__ == "__main__":
    # Run all tests
    test_queue_message()
    whatsapp_messages_queue.wait_until_queue_is_empty()