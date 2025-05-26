from threading import Thread
from queue import Queue
import time
import logging

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
                result = "send successfully" if sended else "wasn't sended"
                logging.info(f"Message {result} to {cellphone}-{wp_id}")
            except Exception as e:
                logging.error(f"Error sending message to {cellphone}: {str(e)}", end="")
                if retry_count < self.MAX_RETRIES:
                    logging.info("Retrying...")
                    retry_count += 1
                else:
                    logging.warning("Max retries reached")
                    break

            self.message_queue.task_done()
            time.sleep(self.CALL_DELAY)

    def put_message(self, cellphone, message, wp_id, retry_count = 0):
        self.message_queue.put((cellphone, message, wp_id, retry_count))

    def stop(self):
        self.message_queue.add_message("", "STOP")
        self.consumer_thread.join()
        
    def wait_until_queue_is_empty(self):
        self.message_queue.join()
        