from flask import Blueprint, request

def create_webhook_blueprint(whatsapp_service):
    blueprint = Blueprint('webhook', __name__)

    @blueprint.route('/webhook', methods=['POST'])
    def webhook():
        data = request.get_json()
        result = whatsapp_service.process_incoming_message(data)

        if result:
            sender_id, message_text = result
            sender_phone = f"+{sender_id.split('@')[0]}"
            whatsapp_service.send_message(
                sender_phone,
                f"[ECHO] Received your message: {message_text}"
            )

        return 'OK', 200

    return blueprint