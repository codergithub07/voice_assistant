"""Experimental real-time speech emotion recognition using Wav2Vec2."""
import torch
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification
from pathlib import Path
import sys

src_path = Path(__file__).resolve().parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from jarvis.config import DEFAULT_VOSK_MODEL

def main():
    print("Loading Vosk and Wav2Vec2 emotion models...")
    vosk_model = Model(str(DEFAULT_VOSK_MODEL))
    recognizer = KaldiRecognizer(vosk_model, 16000)

    model_name = "superb/wav2vec2-base-superb-er"
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    emotion_model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
    emotion_model.to("cpu")
    emotion_model.eval()

    def audio_callback(indata, frames, time_info, status):
        data = indata[:, 0]
        pcm_bytes = data.tobytes()

        # ASR
        if recognizer.AcceptWaveform(pcm_bytes):
            print("\nTranscription:", recognizer.Result())

        # Emotion classification
        inputs = feature_extractor(data, sampling_rate=16000, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = emotion_model(**inputs).logits
        pred_idx = logits.argmax(dim=-1).item()
        label = emotion_model.config.id2label[pred_idx]
        print(f"\rEmotion detected: {label}", end="", flush=True)

    with sd.InputStream(callback=audio_callback, samplerate=16000, channels=1, blocksize=8000):
        print("Listening for emotion analysis... (Ctrl+C to stop)")
        try:
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            print("\nEmotion analysis stopped.")

if __name__ == "__main__":
    main()
