import os
import json
import tiktoken
from openai import OpenAI
from app.chat_provider import ChatProvider


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")




class OpenAiChatProvider(ChatProvider):
    """OpenAI chat provider implementation."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        

    def _get_call_analysis_schema(self):
        return {
            "type": "object",
            "properties": {
                "response": {
                    "type": "string",
                    "additionalProperties": False,
                }
            },
            "required": [
                "response",
            ],
            "additionalProperties": False,
        }

    def _analyze_call_transcript(self, chat_message: str):
        """
        You are an expert chat assitant, take the user message and return a valid and detailed JSON response.

        Args:
            chat_message (str): The message user sent to the AI assistant

        Returns:
            dict: A dictionary containing the analysis results or an error message.
        """
        try:
            # Create a system message with the instructions
            system_message = """
            You are an expert chat assitant, take the user message and return a valid and detailed JSON response.

            Format your response as JSON with the requested structure.
            """

            enc = tiktoken.encoding_for_model("gpt-4o")
            tokens = enc.encode(system_message + chat_message)
            print(f"Token count: {len(tokens)}")

            # Make the API call using the new responses endpoint with input array
            try:
                response = self.client.responses.create(
                    model="gpt-4.1",
                    input=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": chat_message},
                    ],
                    text={
                        "format": {
                            "type": "json_schema",
                            "name": "user_chat",
                            "schema": self._get_call_analysis_schema(),
                            "strict": True,
                        }
                    },
                )

                # Extract and parse the JSON response
                analysis_text = response.output_text
                analysis_json = json.loads(analysis_text)

                return True, analysis_json
            except Exception as api_error:
                print(f"API error: {str(api_error)}")
                return False, {
                    "error": "Failed to analyze transcript. Please try again later."
                }

        except Exception as e:
            # For prototype, return a simple error and fallback response
            print(f"Error analyzing transcript: {str(e)}")
            return False, {
                "error": "An error occurred while processing your request. Please try again later."
            }

    def chat(self, message: str) -> dict:
        success, analysis = self._analyze_call_transcript(message)
        if success:
            return analysis
        else:
            return {"error": analysis.get("error", "Unknown error occurred")}


