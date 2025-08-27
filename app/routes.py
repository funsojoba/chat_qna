from flask import Blueprint, jsonify, request
from app.services import process_user_chat

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the API"})


@api_blueprint.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})



@api_blueprint.route("/chat", methods=["POST"])
def chat_ai():
    data = request.get_json()
    
    provider = data.get("provider", "openai")

    if not data or "q" not in data:
        return jsonify({"error": "Missing required field 'q'"}), 400
    
    message = data["q"]

    response = process_user_chat(message, provider)

    return jsonify(response), 200