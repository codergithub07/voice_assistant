"""Text-to-speech engine supporting offline (pyttsx3) and online (gTTS)."""
import os
import shutil
import tempfile
from typing import Optional

class TTSEngine:
    """Manages speech synthesis for assistant feedback."""

    def __init__(self, engine_type: str = "pyttsx3", rate: int = 165):
        self.engine_type = engine_type
        self.rate = rate
        self._pyttsx_engine = None

        if self.engine_type == "pyttsx3":
            try:
                import pyttsx3
                self._pyttsx_engine = pyttsx3.init()
                self._pyttsx_engine.setProperty("rate", self.rate)
            except Exception as e:
                print(f"[TTS Warning] Could not initialize pyttsx3: {e}. Falling back to console.")
                self.engine_type = "console"

    def speak(self, text: str) -> None:
        """Speak the given text or print it to console."""
        if not text:
            return

        print(f"[Jarvis]: {text}")

        if self.engine_type == "pyttsx3" and self._pyttsx_engine:
            try:
                self._pyttsx_engine.say(text)
                self._pyttsx_engine.runAndWait()
                return
            except Exception as e:
                print(f"[TTS Warning] pyttsx3 error: {e}")

        if self.engine_type == "gtts":
            try:
                from gtts import gTTS
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tf:
                    temp_audio = tf.name
                
                tts = gTTS(text=text, lang="en", slow=False)
                tts.save(temp_audio)

                player = shutil.which("mpg321") or shutil.which("ffplay") or shutil.which("mpv")
                if player:
                    os.system(f"{player} -nodisp -autoexit {temp_audio} > /dev/null 2>&1")
                
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
            except Exception as e:
                print(f"[TTS Warning] gTTS error: {e}")
