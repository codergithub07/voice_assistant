"""Audio input streaming using sounddevice."""
import queue
from typing import Optional
import sounddevice as sd

from jarvis.config import SAMPLE_RATE, BLOCK_SIZE, CHANNELS, DTYPE

class AudioStream:
    """Manages real-time microphone audio capture stream."""
    
    def __init__(
        self,
        samplerate: int = SAMPLE_RATE,
        blocksize: int = BLOCK_SIZE,
        channels: int = CHANNELS,
        dtype: str = DTYPE
    ):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.channels = channels
        self.dtype = dtype
        self.queue: queue.Queue = queue.Queue()
        self._stream: Optional[sd.RawInputStream] = None

    def _callback(self, indata, frames, time_info, status):
        """Audio callback triggered by sounddevice for each block."""
        if status:
            print(f"[Audio Warning] {status}")
        self.queue.put(bytes(indata))

    def start(self) -> None:
        """Start microphone input stream."""
        if self._stream is None:
            self._stream = sd.RawInputStream(
                samplerate=self.samplerate,
                blocksize=self.blocksize,
                dtype=self.dtype,
                channels=self.channels,
                callback=self._callback
            )
            self._stream.start()

    def stop(self) -> None:
        """Stop and close audio stream."""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def get_chunk(self, block: bool = True, timeout: Optional[float] = None) -> bytes:
        """Retrieve next audio bytes chunk from the queue."""
        return self.queue.get(block=block, timeout=timeout)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
