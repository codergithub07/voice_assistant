"""Vosk speech-to-text implementation."""
import json
from pathlib import Path
from typing import Optional
from vosk import Model, KaldiRecognizer

from jarvis.config import DEFAULT_VOSK_MODEL, SAMPLE_RATE
from jarvis.stt.base import BaseSTT

class VoskSTT(BaseSTT):
    """Offline STT powered by Vosk Kaldi speech recognizer."""

    def __init__(
        self,
        model_path: Optional[Path] = None,
        samplerate: int = SAMPLE_RATE,
        grammar: Optional[str] = None
    ):
        self.model_path = Path(model_path) if model_path else DEFAULT_VOSK_MODEL
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Vosk model not found at '{self.model_path}'. "
                "Please download a model to the 'vosk_models/' directory."
            )

        self.model = Model(str(self.model_path))
        self.samplerate = samplerate
        
        if grammar:
            self.recognizer = KaldiRecognizer(self.model, self.samplerate, grammar)
        else:
            self.recognizer = KaldiRecognizer(self.model, self.samplerate)

    def accept_waveform(self, data: bytes) -> bool:
        """Process incoming audio bytes. Returns True if phrase boundary reached."""
        return self.recognizer.AcceptWaveform(data)

    def get_result(self) -> str:
        """Return finalized recognized text string."""
        raw_result = self.recognizer.Result()
        try:
            parsed = json.loads(raw_result)
            return parsed.get("text", "").strip()
        except json.JSONDecodeError:
            return ""

    def get_partial_result(self) -> str:
        """Return partial transcription in progress."""
        raw_partial = self.recognizer.PartialResult()
        try:
            parsed = json.loads(raw_partial)
            return parsed.get("partial", "").strip()
        except json.JSONDecodeError:
            return ""
