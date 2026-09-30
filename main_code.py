"""Legacy entry point.

The application has been restructured into a modular package under `src/jarvis/`.
Please use `python main.py` as the primary entry point.
"""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from main import main

if __name__ == "__main__":
    print("[Notice]: Running via legacy 'main_code.py'. Preferred entry point is 'main.py'.")
    main()