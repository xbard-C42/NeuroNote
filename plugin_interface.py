# core/plugin.py
from abc import ABC, abstractmethod
from typing import Any, Dict

class Plugin(ABC):
    name: str
    description: str

    @abstractmethod
    def applies(self, input_text: str, context: Dict[str, Any]) -> bool:
        """Check if plugin should activate for this input."""
        pass

    @abstractmethod
    def execute(self, input_text: str, context: Dict[str, Any]) -> str:
        """Run the plugin logic and return a string output."""
        pass

# Example plugin implementation
class EchoPlugin(Plugin):
    name = "echo"
    description = "Simply echoes back the input."

    def applies(self, input_text: str, context: Dict[str, Any]) -> bool:
        return "echo" in input_text.lower()

    def execute(self, input_text: str, context: Dict[str, Any]) -> str:
        return f"Echoing back: {input_text}"
