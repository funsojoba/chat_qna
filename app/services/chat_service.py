from app.chat_provider.factory import ChatProviderFactory



def process_user_chat(message: str, provider_name: str = "openai"):
    """
    Service layer for processing user chat messages.
    Decides which provider to call and returns a normalized response.
    """
    try:
        # Get the chat provider instance
        provider = ChatProviderFactory.get_provider(provider_name)
        
        # Call the provider's chat method
        response = provider.chat(message)

        # Normalize the response structure
        if "error" in response:
            return {
                "success": False,
                "provider": provider_name,
                "error": response["error"]
            }

        return {
            "success": True,
            "provider": provider_name,
            "response": response.get("response", "")
        }

    except Exception as e:
        return {
            "success": False,
            "provider": provider_name,
            "error": str(e)
        }