"""Core assistant controller orchestrating STT, NLP, Skills, and TTS."""
import sys
from typing import Optional

from jarvis.audio.stream import AudioStream
from jarvis.config import CONFIDENCE_THRESHOLD
from jarvis.nlp.classifier import IntentClassifier
from jarvis.skills.registry import SkillRegistry
from jarvis.skills.vlc_player import VLCController
from jarvis.skills.weather import WeatherSkill
from jarvis.skills.web_search import WebSkill
from jarvis.stt.vosk_stt import VoskSTT
from jarvis.tts.engine import TTSEngine

class JarvisAssistant:
    """Main coordinator for Jarvis voice assistant."""

    def __init__(
        self,
        enable_tts: bool = True,
        confidence_threshold: float = CONFIDENCE_THRESHOLD
    ):
        print("Initializing Jarvis Assistant...")
        self.confidence_threshold = confidence_threshold
        
        # Audio & STT
        self.audio_stream = AudioStream()
        self.stt = VoskSTT()
        
        # NLP Classifier
        self.classifier = IntentClassifier()
        
        # TTS Engine
        self.tts = TTSEngine() if enable_tts else None
        
        # Skills & Registry
        self.vlc = VLCController()
        self.weather = WeatherSkill()
        self.web = WebSkill()
        self.registry = SkillRegistry()
        
        self._register_default_skills()
        print("Jarvis is ready!")

    def _register_default_skills(self) -> None:
        """Register default intent action handlers."""
        
        @self.registry.register("PlayMusic")
        def handle_play_music(command: str, _):
            # Strip common trigger phrases
            cleaned = command.lower().replace("play music", "").replace("play", "").strip()
            if not cleaned:
                # Toggle play/pause if no track specified
                toggled = self.vlc.play_pause()
                return "Toggled music playback." if toggled else "No music query specified."
            return self.vlc.play_by_query(cleaned)

        @self.registry.register("GetWeather")
        def handle_weather(command: str, _):
            # Extract simple city if present (e.g., 'weather in paris')
            words = command.lower().split()
            city = None
            if "in" in words:
                idx = words.index("in")
                if idx + 1 < len(words):
                    city = " ".join(words[idx+1:])
            return self.weather.get_weather(city)

        @self.registry.register("SearchCreativeWork")
        def handle_search(command: str, _):
            query = command.lower().replace("search", "").strip()
            return self.web.search_google(query or command)

        @self.registry.register("BookRestaurant")
        def handle_restaurant(command: str, _):
            return "Restaurant booking capability is noted. Opening reservation browser..."

        @self.registry.register("AddToPlaylist")
        def handle_playlist(command: str, _):
            return "Added to playlist queue."

    def speak(self, text: str) -> None:
        """Speak response or print to stdout."""
        if self.tts:
            self.tts.speak(text)
        else:
            print(f"[Jarvis]: {text}")

    def handle_intent(self, intent: str, confidence: float, command_text: str) -> None:
        """Process detected intent above threshold."""
        print(f"\n[Detected Intent]: {intent} (Confidence: {confidence:.2f})")
        print(f"[Command]: {command_text}")

        response = self.registry.dispatch(intent, command_text)
        if response:
            self.speak(response)

    def run(self) -> None:
        """Run listening loop until interrupted."""
        print("\nListening for voice commands... (Press Ctrl+C to stop)")
        self.audio_stream.start()

        try:
            while True:
                data = self.audio_stream.get_chunk()
                
                if self.stt.accept_waveform(data):
                    text = self.stt.get_result()
                    if text:
                        print(f"\n[User]: {text}")
                        try:
                            intent, confidence = self.classifier.predict_with_confidence(text)
                            if confidence >= self.confidence_threshold:
                                self.handle_intent(intent, confidence, text)
                            else:
                                print(f"[Jarvis]: Low confidence ({confidence:.2f}) for '{text}' - please repeat.")
                        except Exception as e:
                            print(f"[Error]: Failed to process intent: {e}")

                    print("\nListening...", flush=True)
                else:
                    partial = self.stt.get_partial_result()
                    if partial:
                        sys.stdout.write(f"\r[Hearing]: {partial}")
                        sys.stdout.flush()

        except KeyboardInterrupt:
            print("\nShutting down Jarvis...")
        finally:
            self.audio_stream.stop()
            print("Jarvis terminated safely.")
