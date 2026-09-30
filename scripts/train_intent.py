"""Train Intent Classification model using SNIPS dataset."""
import json
import os
import re
import sys
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

# Add 'src' to python path
src_path = Path(__file__).resolve().parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from jarvis.config import DATASETS_DIR, TRAINED_MODELS_DIR
from jarvis.nlp.preprocessor import TextPreprocessor

def parse_snips_data(base_path: Path) -> pd.DataFrame:
    """Parse SNIPS-style intent classification JSON files."""
    intents = [d for d in os.listdir(base_path) if os.path.isdir(base_path / d)]
    data = []

    for intent in intents:
        intent_path = base_path / intent
        for file_name in os.listdir(intent_path):
            if not file_name.endswith(".json"):
                continue
            file_path = intent_path / file_name
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="latin-1") as f:
                    json_data = json.load(f)
            except Exception as e:
                print(f"Skipping {file_path}: {e}")
                continue

            examples = json_data.get(intent, list(json_data.values())[0] if json_data else [])

            for example in examples:
                if "data" not in example:
                    continue
                entities = []
                text_parts = []
                for item in example["data"]:
                    text_parts.append(item["text"])
                    if "entity" in item:
                        entities.append((item["text"], item["entity"]))
                full_text = " ".join(text_parts)
                cleaned_text = re.sub(r"\s+", " ", full_text).strip()
                data.append((cleaned_text, intent, entities))

    return pd.DataFrame(data, columns=["text", "intent", "entities"])

def main():
    dataset_path = DATASETS_DIR / "intent_classification_dataset"
    if not dataset_path.exists():
        print(f"Error: Dataset directory '{dataset_path}' not found.")
        sys.exit(1)

    print(f"Loading dataset from '{dataset_path}'...")
    df = parse_snips_data(dataset_path)
    print(f"Loaded {len(df)} samples across {df['intent'].nunique()} intents.")

    # Use unified preprocessor with lemmatization
    preprocessor = TextPreprocessor(method="lemmatize")
    print("Preprocessing text...")
    df["processed"] = df["text"].apply(preprocessor.preprocess)

    # Label Encoding
    le = LabelEncoder()
    y = le.fit_transform(df["intent"])

    # TF-IDF Vectorization
    print("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=2500,
        ngram_range=(1, 2),
        stop_words="english"
    )
    X = vectorizer.fit_transform(df["processed"])

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train LinearSVC
    print("Training LinearSVC model...")
    model = LinearSVC(
        class_weight="balanced",
        dual=False,
        max_iter=5000
    )
    model.fit(X_train, y_train)

    # Evaluate
    print("\n--- Evaluation Report ---")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Save artifacts
    TRAINED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, TRAINED_MODELS_DIR / "intent_model.joblib")
    joblib.dump(vectorizer, TRAINED_MODELS_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(le, TRAINED_MODELS_DIR / "label_encoder.joblib")
    print(f"Successfully saved models to '{TRAINED_MODELS_DIR}'.")

if __name__ == "__main__":
    main()
