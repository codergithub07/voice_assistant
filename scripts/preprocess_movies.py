"""Preprocess movie titles for ASR / language model dictionaries."""
import sys
from pathlib import Path

# Add 'src' to python path
src_path = Path(__file__).resolve().parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from jarvis.config import PROJECT_ROOT
from jarvis.nlp.preprocessor import TextPreprocessor

def main():
    input_file = PROJECT_ROOT / "movies.txt"
    output_file = PROJECT_ROOT / "scripts" / "preprocessed_movies.txt"

    if not input_file.exists():
        print(f"Error: {input_file} not found. Run scripts/scrape_movies.py first.")
        sys.exit(1)

    preprocessor = TextPreprocessor(method="lemmatize")
    print(f"Reading '{input_file}'...")
    with open(input_file, "r", encoding="utf-8") as f:
        movies = f.readlines()

    print(f"Preprocessing {len(movies)} movie titles...")
    processed_movies = []
    for line in movies:
        cleaned = preprocessor.clean_text(line)
        with_numbers = preprocessor.convert_digits(cleaned)
        final_line = " ".join(with_numbers.split())
        if final_line:
            processed_movies.append(final_line)

    with open(output_file, "w", encoding="utf-8") as f:
        for m in processed_movies:
            f.write(f"{m}\n")

    print(f"✓ Saved preprocessed titles to '{output_file}'")

if __name__ == "__main__":
    main()
