"""Speech-to-text module."""
from jarvis.stt.base import BaseSTT
from jarvis.stt.vosk_stt import VoskSTT

__all__ = ["BaseSTT", "VoskSTT"]
