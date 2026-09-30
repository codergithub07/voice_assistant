# Jarvis Voice Assistant (mark_0)

An offline-first, modular desktop voice assistant powered by Vosk speech recognition, scikit-learn intent classification, and Linux system automation.

## Project Structure

```
mark_0/
├── src/
│   └── jarvis/
│       ├── __init__.py
│       ├── config.py              # Centralized configuration (audio, paths, thresholds)
│       ├── audio/
│       │   ├── __init__.py
│       │   └── stream.py          # Real-time microphone audio capture stream
│       ├── stt/
│       │   ├── __init__.py
│       │   ├── base.py            # Base ASR interface
│       │   └── vosk_stt.py        # Vosk KaldiRecognizer STT implementation
│       ├── tts/
│       │   ├── __init__.py
│       │   └── engine.py          # Speech synthesis engine (pyttsx3 / gTTS)
│       ├── nlp/
│       │   ├── __init__.py
│       │   ├── preprocessor.py    # Unified text preprocessing (lemmatization & cleaning)
│       │   └── classifier.py      # Intent classifier with confidence scoring
│       ├── skills/
│       │   ├── __init__.py
│       │   ├── registry.py        # Dynamic skill dispatcher
│       │   ├── vlc_player.py      # VLC media player D-Bus MPRIS & file launcher
│       │   ├── weather.py         # OpenWeatherMap weather reporting
│       │   └── web_search.py      # Web navigation and Google / YouTube searches
│       └── core/
│           ├── __init__.py
│           └── assistant.py       # Main event loop orchestrator
├── scripts/                       # Training, preprocessing & scraping tools
│   ├── train_intent.py            # SNIPS dataset training pipeline
│   ├── scrape_movies.py           # Movie name scraper (IMDb, TMDB, Letterboxd)
│   ├── preprocess_movies.py       # Movie titles lexicon preprocessing
│   └── audio_processor.py         # Audio normalization and silence chunking
├── experiments/                   # Prototypes & research code
│   ├── emotion_detection.py       # Speech emotion recognition (Wav2Vec2)
│   └── whisper_test.py            # Faster-Whisper streaming test
├── trained_models/                # Serialized intent models (.joblib)
├── vosk_models/                   # Downloaded Vosk acoustic/language models
├── datasets/                      # Training datasets (SNIPS, EMO-DB)
├── main.py                        # Application entry point
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules
└── pyproject.toml                 # Dependencies and project metadata
```

## Quickstart

### 1. Installation
Install dependencies using `uv`:
```bash
uv sync
```
Or with standard `pip`:
```bash
pip install -e .
```

### 2. Configuration
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Fill in any desired options (e.g. `OPENWEATHER_API_KEY`, `MEDIA_DIR`).

### 3. Running Jarvis
Run the main assistant loop:
```bash
python main.py
```

### 4. Training Intent Classifier
To retrain the intent classification model using the SNIPS dataset:
```bash
python scripts/train_intent.py
```
