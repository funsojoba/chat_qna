from abc import ABC, abstractmethod

class ChatProvider(ABC):
    """Abstract interface for all chat providers."""

    @abstractmethod
    def chat(self, message: str) -> dict:
        """Send a message and return the response."""
        pass