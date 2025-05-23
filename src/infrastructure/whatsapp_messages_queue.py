from threading import Thread
from queue import Queue
import time

class WhatsappMessagesQueue:

    MAX_RETRIES = 3
    CALL_DELAY = 2
    
    def __init__(self, whatsapp_service):
        self.whatsapp_service = whatsapp_service
        self.message_queue = Queue()
        
        self.consumer_thread = Thread(target=self.message_consumer, daemon=True)
        self.consumer_thread.start()

    def message_consumer(self):
        while True:
            cellphone, message, wp_id, retry_count = self.message_queue.get()  # Blocks until a message is available
            if message == "STOP":
                break

            sended = False
            try:
                sended = self.whatsapp_service.send_message(cellphone, message)
            except Exception as e:
                print(f"Error sending message to {cellphone}: {str(e)}", end="")

            if(not sended and retry_count < self.MAX_RETRIES):
                self.put_message(cellphone, message, wp_id, retry_count + 1)
                print("Retrying...")
            elif(not sended and retry_count >= self.MAX_RETRIES):
                print("Max retries reached")
            else:
                print(f"Message sent successfully to {cellphone}-{wp_id}")

            self.message_queue.task_done()
            time.sleep(self.CALL_DELAY)

    def put_message(self, cellphone, message, wp_id, retry_count = 0):
        self.message_queue.put((cellphone, message, wp_id, retry_count))

    def stop(self):
        self.message_queue.add_message("", "STOP")
        self.consumer_thread.join()
        
    def wait_until_queue_is_empty(self):
        self.message_queue.join()
        