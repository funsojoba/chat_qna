import os
import json
import tiktoken
from openai import OpenAI
from app.chat_provider import ChatProvider

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class OpenAiChatProvider(ChatProvider):
    """OpenAI chat provider implementation using the Responses API."""

    def __init__(self, model="gpt-4.1"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def _get_call_analysis_schema(self):
        """
        JSON schema to ensure the model always returns a structured response.
        """
        return {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    "description": "The assistant's response to the user."
                }
            },
            "required": ["response"],
            "additionalProperties": False,
        }

    def _chat_with_ai(self, chat_message: str, history: list = None):
        """
        Calls OpenAI's Responses API and returns a structured JSON response.

        Args:
            chat_message (str): The latest user message.
            history (list): Previous conversation messages.
        """
        try:
            # Create a system prompt
            system_message = """
            You are an expert chat assistant. Take the user's message and return a valid,
            helpful, and structured JSON response based on the schema provided.
            """

            # Combine history + current message
            messages = [{"role": "system", "content": system_message}]
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": chat_message})

            # Token count for debugging (optional)
            try:
                enc = tiktoken.encoding_for_model("gpt-4o")
                tokens = enc.encode(system_message + chat_message)
                print(f"Token count: {len(tokens)}")
            except Exception:
                pass  # If tiktoken fails, ignore — doesn't break the chat flow

            # Call the OpenAI Responses API
            response = self.client.responses.create(
                model=self.model,
                input=messages,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "user_chat",
                        "schema": self._get_call_analysis_schema(),
                        "strict": True,
                    }
                },
            )

            # Extract structured JSON output
            analysis_text = response.output_text
            analysis_json = json.loads(analysis_text)

            return True, analysis_json

        except Exception as api_error:
            print(f"API error: {str(api_error)}")
            return False, {"error": "Failed to get a valid response from OpenAI."}

    def chat(self, message: str, history: list = None) -> dict:
        """
        Public method that handles AI chat requests.
        """
        success, analysis = self._chat_with_ai(message, history)
        if success:
            return analysis
        return {"error": analysis.get("error", "Unknown error occurred")}