from abc import ABC, abstractmethod


class ModelProvider(ABC):
    """Abstract base class for AI model providers."""
    
    @abstractmethod
    def summarize(self, delta: str) -> str:
        """Summarize git diff delta."""
        pass
