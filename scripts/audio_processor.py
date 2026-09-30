"""Audio preprocessing utilities: silence splitting and loudness normalization."""
import os
import sys
from pathlib import Path
from pydub import AudioSegment, silence
from pydub.effects import normalize

def split_audio_on_silence(
    input_wav: Path,
    output_dir: Path,
    min_silence_len: int = 700,
    silence_thresh: int = -40
) -> list:
    """Split an audio file into chunks based on silence boundaries."""
    output_dir.mkdir(parents=True, exist_ok=True)
    audio = AudioSegment.from_file(str(input_wav), format="wav")
    chunks = silence.split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )

    exported_paths = []
    for i, chunk in enumerate(chunks):
        out_file = output_dir / f"chunk_{i}.wav"
        chunk.export(
            str(out_file),
            format="wav",
            parameters=["-ac", "1", "-ar", "16000", "-sample_fmt", "s16"]
        )
        exported_paths.append(out_file)
        print(f"Exported chunk {i} -> {out_file}")

    return exported_paths

def normalize_audio(input_wav: Path, output_wav: Path) -> Path:
    """Normalize loudness of a wav file and resample to 16kHz mono."""
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    audio = AudioSegment.from_file(str(input_wav), format="wav")
    normalized = normalize(audio)
    normalized.export(
        str(output_wav),
        format="wav",
        parameters=["-ac", "1", "-ar", "16000", "-sample_fmt", "s16"]
    )
    print(f"Exported normalized audio -> {output_wav}")
    return output_wav

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audio_processor.py <path_to_wav>")
        sys.exit(0)
    wav_path = Path(sys.argv[1])
    if wav_path.exists():
        split_audio_on_silence(wav_path, wav_path.parent / "chunks")
