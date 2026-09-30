"""Experimental Faster-Whisper real-time streaming test."""
import queue
import sounddevice as sd
import numpy as np

def main():
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Please install faster-whisper to run this experiment.")
        return

    print("Loading Faster-Whisper model...")
    # Can use small, base, or tiny
    model = WhisperModel("base", device="cpu", compute_type="int8")

    samplerate = 16000
    block_duration = 0.5
    q = queue.Queue()

    def callback(indata, frames, time_info, status):
        q.put(indata.copy())

    print("Listening with Faster-Whisper... Speak now")
    buffer = []

    with sd.InputStream(samplerate=samplerate, channels=1, callback=callback):
        try:
            while True:
                data = q.get()
                buffer.append(data)

                # Process every ~1.5 seconds of audio
                if len(buffer) * block_duration >= 1.5:
                    audio_chunk = np.concatenate(buffer, axis=0).flatten()
                    buffer = []

                    segments, _ = model.transcribe(
                        audio_chunk,
                        language="en",
                        beam_size=1,
                        vad_filter=True
                    )
                    for s in segments:
                        print(">>", s.text)
        except KeyboardInterrupt:
            print("\nWhisper experiment stopped.")

if __name__ == "__main__":
    main()
