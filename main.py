"""Main entry point for Jarvis Voice Assistant."""
import sys
from pathlib import Path

# Add 'src' to python path for clean direct execution
src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from jarvis.core.assistant import JarvisAssistant

def main():
    """Start the assistant loop."""
    try:
        assistant = JarvisAssistant()
        assistant.run()
    except Exception as e:
        print(f"[Fatal Error]: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
