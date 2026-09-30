import os
import difflib
import subprocess
import vosk
import sys
import json
import pyaudio
import file_access

# Initialize offline speech recognition with Vosk
model = vosk.Model("models/vosk-model-en-in-0.5")
rec = vosk.KaldiRecognizer(model, 16000)

def listen_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    
    print("Listening...")
    result_text = ""
    while True: 
        data = stream.read(4096)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            result_text += res.get("text", "") + " "
            break  # or continue for longer phrases
    stream.stop_stream()
    
    stream.close()
    p.terminate()
    return result_text.strip()

def extract_keywords(command_text):
    # For a simple case, assume keywords are the words after 'start'
    tokens = command_text.lower().split()
    if "start" in tokens:
        idx = tokens.index("start")
        # assuming that the next words up to "movie" form the title
        try:
            movie_idx = tokens.index("movie", idx)
            keywords = tokens[idx+1:movie_idx]
        except ValueError:
            keywords = tokens[idx+1:]
        return keywords
    return []

def find_best_matching_file(keywords, directory):
    best_match = None
    best_score = 0
    for file in os.listdir(directory):
        file_lower = file.lower()
        # Combine keywords to form a candidate string
        keyword_string = " ".join(keywords)
        score = difflib.SequenceMatcher(None, keyword_string, file_lower).ratio()
        if score > best_score:
            best_score = score
            best_match = file
    return best_match, best_score

def main():
    # Listen to the user's voice command
    command_text = listen_audio()
    print("You said:", command_text)
    
    # Extract keywords from the command
    keywords = extract_keywords(command_text)
    print("Extracted keywords:", keywords)
    
    # Search for the best matching file in the directory
    directory = "/media/tony/ddrive/Movies"
    best_match, score = find_best_matching_file(keywords, directory)
    
    if best_match and score > 0.2:  # Adjust threshold as needed
        print("Best match found:", best_match)
        print("Match score:", score)
        print("Playing file:", best_match)
        # Start the file (for example, using VLC)
        file_access.open_vlc(os.path.join(directory, best_match))
    else:
        print("No matching file found.")

if __name__ == "__main__":
    main()
