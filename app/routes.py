from flask import Blueprint, jsonify, request
from app.services import process_user_chat

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the API"})


@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})



@api_blueprint.route("/api/chat", methods=["POST"])
def chat_ai():
    data = request.get_json()
    
    provider = data.get("provider", "openai")

    if not data or "message" not in data:
        return jsonify({"error": "Missing required field 'message'"}), 400
    
    message = data["message"]
    session_id = data.get("session_id", "default_session")

    response = process_user_chat(session_id, message, provider)

    return jsonify(response), 200