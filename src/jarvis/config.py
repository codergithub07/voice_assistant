"""Configuration settings for Jarvis voice assistant."""
import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRAINED_MODELS_DIR = Path(os.getenv("TRAINED_MODELS_DIR", PROJECT_ROOT / "trained_models"))
VOSK_MODELS_DIR = Path(os.getenv("VOSK_MODELS_DIR", PROJECT_ROOT / "vosk_models"))
DATASETS_DIR = Path(os.getenv("DATASETS_DIR", PROJECT_ROOT / "datasets"))

# Audio Configuration
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", 16000))
BLOCK_SIZE = int(os.getenv("BLOCK_SIZE", 8000))
CHANNELS = int(os.getenv("AUDIO_CHANNELS", 1))
DTYPE = "int16"

# STT Configuration
DEFAULT_VOSK_MODEL = VOSK_MODELS_DIR / "vosk-model-small-en-us-0.15"

# NLP Configuration
CONFIDENCE_THRESHOLD = float(os.getenv("INTENT_CONFIDENCE_THRESHOLD", 0.55))

# Media / VLC Configuration
DEFAULT_MEDIA_DIR = Path(os.getenv("MEDIA_DIR", "/media/tony/ddrive/Movies"))

# External Services
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_DEFAULT_CITY = os.getenv("OPENWEATHER_DEFAULT_CITY", "London")
