"""Abstract base class for Speech-To-Text engines."""
from abc import ABC, abstractmethod
from typing import Optional, Tuple

class BaseSTT(ABC):
    """Interface for Speech-to-Text recognizers."""

    @abstractmethod
    def accept_waveform(self, data: bytes) -> bool:
        """Process incoming audio bytes. Returns True if full utterance completed."""
        pass

    @abstractmethod
    def get_result(self) -> str:
        """Return final transcribed text for the utterance."""
        pass

    @abstractmethod
    def get_partial_result(self) -> str:
        """Return intermediate / real-time partial transcription."""
        pass
