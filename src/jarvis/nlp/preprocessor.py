"""Unified text preprocessing for training and inference."""
import re
import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer

class TextPreprocessor:
    """Preprocesses text for NLU / Intent classification tasks."""
    
    def __init__(self, method: str = "lemmatize"):
        """
        Initialize preprocessor.
        :param method: 'lemmatize' (WordNetLemmatizer) or 'stem' (PorterStemmer)
        """
        self.method = method
        if method == "lemmatize":
            try:
                nltk.download("wordnet", quiet=True)
                self.normalizer = WordNetLemmatizer()
            except Exception:
                self.normalizer = WordNetLemmatizer()
        elif method == "stem":
            self.normalizer = PorterStemmer()
        else:
            raise ValueError(f"Unknown normalization method: {method}")

    def clean_text(self, text: str) -> str:
        """Sanitize encoding, lowercase, and strip punctuation."""
        if not text:
            return ""
        # Handle Latin-1/UTF-8 inconsistencies if present
        text = text.encode("latin-1", "ignore").decode("utf-8", "ignore")
        text = text.lower()
        # Keep only alphanumeric characters and spaces
        text = re.sub(r"[^a-z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def convert_digits(self, text: str) -> str:
        """Convert digits in text to words (e.g., '2' -> 'two')."""
        try:
            from num2words import num2words
            tokens = text.split()
            converted = [num2words(int(w)) if w.isdigit() else w for w in tokens]
            return " ".join(converted)
        except ImportError:
            return text

    def normalize_tokens(self, text: str) -> str:
        """Tokenize and apply lemmatization or stemming."""
        tokens = text.split()
        if self.method == "lemmatize":
            processed = [self.normalizer.lemmatize(w) for w in tokens if len(w) > 2]
        else:
            processed = [self.normalizer.stem(w) for w in tokens if len(w) > 2]
        return " ".join(processed)

    def preprocess(self, text: str, convert_numbers: bool = False) -> str:
        """Full preprocessing pipeline."""
        text = self.clean_text(text)
        if convert_numbers:
            text = self.convert_digits(text)
        return self.normalize_tokens(text)


# Default shared instance using lemmatization (matching trained SNIPS model)
_default_preprocessor = TextPreprocessor(method="lemmatize")

def preprocess_text(text: str, method: str = "lemmatize") -> str:
    """Convenience helper function for text preprocessing."""
    if method == "lemmatize":
        return _default_preprocessor.preprocess(text)
    return TextPreprocessor(method=method).preprocess(text)
