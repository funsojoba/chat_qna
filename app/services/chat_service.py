from app.chat_provider.factory import ChatProviderFactory



conversation_store = {}
def process_user_chat(session_id: str, message: str, provider_name: str = "openai"):
    """
    Service layer for processing user chat messages.
    Handles:
      - Dynamic provider switching (via factory)
      - Conversation history management
      - Normalized responses
    """

    try:
        # Retrieve the chat provider instance
        provider = ChatProviderFactory.get_provider(provider_name)

        # Fetch conversation history for this session
        history = conversation_store.get(session_id, [])

        # Send the message + history to the provider
        response = provider.chat(message=message, history=history)

        print()

        # Check for provider-level errors
        if isinstance(response, dict) and "error" in response:
            return {
                "success": False,
                "provider": provider_name,
                "error": response["error"],
                "history": history
            }

        # Update the conversation history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response.get("response", response)})

        # Save updated history back into store
        conversation_store[session_id] = history

        # Return normalized response structure
        return {
            "success": True,
            "provider": provider_name,
            "response": response.get("response", response),
            "history": history
        }

    except Exception as e:
        return {
            "success": False,
            "provider": provider_name,
            "error": str(e),
            "history": conversation_store.get(session_id, [])
        }