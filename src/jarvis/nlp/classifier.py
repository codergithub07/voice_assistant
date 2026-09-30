"""Intent classification module using scikit-learn models."""
from pathlib import Path
from typing import Tuple, Optional
import joblib
import numpy as np

from jarvis.config import TRAINED_MODELS_DIR
from jarvis.nlp.preprocessor import TextPreprocessor

class IntentClassifier:
    """Classifies user spoken query into intent with confidence score."""
    
    def __init__(
        self,
        model_dir: Optional[Path] = None,
        preprocessing_method: str = "lemmatize"
    ):
        self.model_dir = Path(model_dir) if model_dir else TRAINED_MODELS_DIR
        self.preprocessor = TextPreprocessor(method=preprocessing_method)
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self._load_models()

    def _load_models(self) -> None:
        """Load serialized model, TF-IDF vectorizer, and label encoder."""
        model_path = self.model_dir / "intent_model.joblib"
        vectorizer_path = self.model_dir / "tfidf_vectorizer.joblib"
        le_path = self.model_dir / "label_encoder.joblib"

        if not (model_path.exists() and vectorizer_path.exists() and le_path.exists()):
            raise FileNotFoundError(
                f"Missing model files in '{self.model_dir}'. "
                "Ensure intent_model.joblib, tfidf_vectorizer.joblib, and label_encoder.joblib are present."
            )

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.label_encoder = joblib.load(le_path)

    def predict(self, text: str) -> str:
        """Predict intent name for a given raw text string."""
        intent, _ = self.predict_with_confidence(text)
        return intent

    def predict_with_confidence(self, text: str) -> Tuple[str, float]:
        """
        Predict intent and calculate confidence score via sigmoid of decision function.
        :return: (intent_name, confidence_score)
        """
        processed = self.preprocessor.preprocess(text)
        if not processed.strip():
            return "Unknown", 0.0

        vectorized = self.vectorizer.transform([processed])
        decision_scores = self.model.decision_function(vectorized)[0]
        intent_idx = self.model.predict(vectorized)[0]
        intent = self.label_encoder.inverse_transform([intent_idx])[0]

        # Calculate confidence using sigmoid on decision value
        if hasattr(decision_scores, "__len__"):
            score = decision_scores[intent_idx]
        else:
            score = decision_scores
        confidence = float(1 / (1 + np.exp(-score)))

        return intent, confidence
