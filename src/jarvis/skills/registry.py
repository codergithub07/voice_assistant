"""Skill registry and intent dispatcher."""
from typing import Callable, Dict, Any, Optional

class SkillRegistry:
    """Registry mapping intent names to action callback functions."""

    def __init__(self):
        self._handlers: Dict[str, Callable[[str, Any], Optional[str]]] = {}

    def register(self, intent_name: str):
        """Decorator to register a function as a handler for an intent."""
        def decorator(func: Callable[[str, Any], Optional[str]]):
            self._handlers[intent_name] = func
            return func
        return decorator

    def dispatch(self, intent: str, command_text: str, context: Optional[Any] = None) -> Optional[str]:
        """Dispatch detected intent to its registered handler."""
        handler = self._handlers.get(intent)
        if handler:
            return handler(command_text, context)
        print(f"[Skill Warning] No handler registered for intent: '{intent}'")
        return f"I recognized the intent '{intent}', but no action handler is configured."
