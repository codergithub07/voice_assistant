import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import joblib
import re
from nltk.stem import PorterStemmer
import numpy as np

# Load your trained intent classification model
class IntentClassifier:
    def __init__(self, model_path="model"):
        self.model = joblib.load(f"{model_path}/intent_model.joblib")
        self.vectorizer = joblib.load(f"{model_path}/tfidf_vectorizer.joblib")
        self.le = joblib.load(f"{model_path}/label_encoder.joblib")
        self.stemmer = PorterStemmer()
        
    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        tokens = text.split()
        tokens = [self.stemmer.stem(word) for word in tokens if len(word) > 2]
        return " ".join(tokens)
    
    def predict(self, text):
        processed = self.preprocess(text)
        vectorized = self.vectorizer.transform([processed])
        intent_idx = self.model.predict(vectorized)[0]
        return self.le.inverse_transform([intent_idx])[0]
    
    def predict_with_confidence(self, text):
        processed = self.preprocess(text)
        vectorized = self.vectorizer.transform([processed])
        probabilities = self.model.decision_function(vectorized)[0]
        intent_idx = self.model.predict(vectorized)[0]
        intent = self.le.inverse_transform([intent_idx])[0]
        confidence = 1 / (1 + np.exp(-probabilities[intent_idx]))
        return intent, confidence

# Initialize the intent classifier
intent_classifier = IntentClassifier(model_path="trained_models")

# Load Vosk model
model = Model(r"vosk_models/vosk-model-small-en-us-0.15")  
rec = KaldiRecognizer(model, 16000)

# Configure audio stream
q = queue.Queue()
def callback(indata, frames, time, status):
    if status: print(status)
    q.put(bytes(indata))

stream = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback)
stream.start()

def handle_intent(intent, text):
    """Execute actions based on detected intent"""
    print(f"\nDetected intent: {intent}")
    print(f"Command: {text}")
    
    # Add your action handlers here
    if intent == "PlayMusic":
        # Extract song/artist and play
        print("Playing music...")
        
    elif intent == "BookRestaurant":
        # Extract reservation details
        print("Booking restaurant...")
        
    elif intent == "GetWeather":
        # Extract location and get weather
        print("Getting weather...")
        
    # Add more intent handlers...

print("Listening... Say something!")
while True:
    data = q.get()
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get("text", "").strip()
        
        if text:  # Only process if we have speech input
            print(f"\nRecognized: {text}")
            
            # Get intent with confidence
            try:
                intent, confidence = intent_classifier.predict_with_confidence(text)
                
                if confidence > 0.55:  # Confidence threshold
                    handle_intent(intent, text)
                else:
                    print(f"Low confidence ({confidence:.2f}) - please repeat")
            except Exception as e:
                print(f"Error processing intent: {str(e)}")
                
        print("\nListening...")
    else:
        # Process partial results for real-time feedback
        partial = json.loads(rec.PartialResult())
        if "partial" in partial:
            print(f"\rProcessing: {partial['partial']}", end="", flush=True)