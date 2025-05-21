from flask import Blueprint, request, jsonify

def create_text_chat_agent_blueprint(text_chat_agent):
    blueprint = Blueprint('text_chat_agent_api', __name__)

    @blueprint.route('/text_chat_agent_api', methods=['POST'])
    def text_chat_agent_api():
        data = request.get_json()
        thread_id = data.get("thread_id")
        message = data.get("message")

        if not thread_id or not message:
            return jsonify({"error": "Missing 'thread_id' or 'message'"}), 400

        text_chat_agent.set_thread_id(thread_id)

        try:
            response = text_chat_agent.process_message(message)
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return blueprint