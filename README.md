# Jarvis - Offline Voice Assistant

An offline-first, modular desktop voice assistant built in Python. Powered by Vosk (Kaldi ASR) for local speech recognition, Scikit-Learn for intent classification, and D-Bus/subprocess automation for Linux desktop and VLC media controls.

---

## Project Structure

```text
mark_0/
├── jarvis/                         # Core Python package
│   ├── config.py                   # Centralized configuration (.env loader)
│   ├── assistant.py                # JarvisAssistant orchestrator
│   ├── audio/                      # Real-time microphone capture & queue streaming
│   │   └── recorder.py
│   ├── stt/                        # Speech-To-Text engines (Vosk, Kaldi)
│   │   ├── base.py
│   │   └── vosk_stt.py
│   ├── tts/                        # Text-To-Speech synthesis (pyttsx3, gTTS fallback)
│   │   └── engine.py
│   ├── nlp/                        # NLP and Intent Classification
│   │   ├── preprocessor.py         # Unified text preprocessor for train & inference
│   │   └── intent_classifier.py    # Intent classifier with confidence scoring
│   └── skills/                     # Modular action handlers
│       ├── base.py
│       ├── vlc_player.py           # VLC playback & fuzzy media matching
│       ├── weather.py              # OpenWeatherMap API skill
│       ├── system_control.py       # Browser and system commands
│       └── registry.py             # Skill dispatcher
│
├── scripts/                        # Standalone developer tools
│   ├── train_intent_model.py       # Trains intent classifier on SNIPS dataset
│   ├── scrape_movies.py            # Movie title scraper for ASR lexicon customization
│   └── audio_preprocessor.py       # PyDub silence-splitting and audio normalization
│
├── trained_models/                 # Serialized model weights (Joblib)
│   ├── intent_model.joblib
│   ├── tfidf_vectorizer.joblib
│   └── label_encoder.joblib
│
├── resources/                      # Lexicons, dictionaries, and movie lists
├── tests/                          # Automated tests
├── .env.example                    # Environment configuration template
├── .gitignore                      # Git ignore rules for caches, media, and weights
├── main.py                         # Primary application entry point
├── main_code.py                    # Backwards-compatible legacy entry point
└── pyproject.toml                  # Project metadata and dependencies
```

---

## Getting Started

### 1. Requirements & Dependencies
Make sure you have `uv` installed, then install dependencies:

```bash
uv sync
```

### 2. Configure Environment
Copy `.env.example` to `.env` and adjust paths or API keys:

```bash
cp .env.example .env
```

Key variables in `.env`:
* `VOSK_MODEL_PATH`: Path to your downloaded Vosk model directory (e.g. `vosk_models/vosk-model-small-en-us-0.15`).
* `MEDIA_DIRECTORY`: Directory containing movie and music files for VLC.
* `OPENWEATHER_API_KEY`: (Optional) API key from OpenWeatherMap.

---

## Running Jarvis

### Voice Mode (Default)
Run with your microphone connected:
```bash
python main.py
```

### Interactive Text Mode (Testing without microphone)
Test intent recognition and skill execution directly from the terminal:
```bash
python main.py --text-mode
```

### Set Custom Confidence Threshold
```bash
python main.py --confidence 0.60
```

---

## Retraining the Intent Model
To retrain the intent classification model using the unified preprocessor:
```bash
python scripts/train_intent_model.py
```
This updates the models in `trained_models/`.
