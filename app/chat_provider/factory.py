from app.chat_provider.openai_provider import OpenAiChatProvider
# from app.chat_providers.gemini_provider import GeminiChatProvider  # Later if needed

class ChatProviderFactory:
    @staticmethod
    def get_provider(provider_name: str):
        providers = {
            "openai": OpenAiChatProvider,
            # "gemini": GeminiChatProvider,
        }

        provider_class = providers.get(provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown provider: {provider_name}")

        return provider_class()