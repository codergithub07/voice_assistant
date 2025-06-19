import json
import queue
import sounddevice as sd  # or use pyaudio
from vosk import Model, KaldiRecognizer
import re

# Load Vosk model (download an English model folder beforehand)
model = Model(r"models/vosk-model-small-en-us-0.15")  
rec = KaldiRecognizer(model, 16000)

# Configure audio stream
q = queue.Queue()
def callback(indata, frames, time, status):
    if status: print(status)
    q.put(bytes(indata))

stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback)
stream.start()

def normalize_offline(text) -> str:
    text = text.lower().strip()
    # remove common fillers
    text = re.sub(r'\b(um|uh|like|you know|can you|please|thank you|i want|do|i want you to)\b', '', text)
    text = re.sub(r'[^\w\s\'\"]+', '', text)
    return text

def normalize_online(text) -> str:
    text = text.lower().strip()
    # remove common fillers
    text = re.sub(r'\b(um|uh|)\b', '', text)
    text = re.sub(r'[^\w\s\'\"]+', '', text)
    return text

print("Listening...")
while True:
    data = q.get()
    if rec.AcceptWaveform(data):
        result = json.loads(rec.FinalResult())
        text = result.get("text", "")
        print("You said:", text)
        print("Listening...")
        # [Process text here: emotion, intent, tasks...]
    # else:
    #     # Partial result can be processed too
    #     partial = json.loads(rec.PartialResult())
    #     # print("Partial:", partial.get("partial", ""))