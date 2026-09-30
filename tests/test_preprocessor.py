"""
Tests for TextPreprocessor in src/jarvis/nlp/preprocessor.py.
"""

import unittest
from jarvis.nlp.preprocessor import TextPreprocessor


class TestTextPreprocessor(unittest.TestCase):

    def test_clean_text(self):
        tp = TextPreprocessor(method="stem")
        raw = "Hello, World! This is a TEST 123...   "
        cleaned = tp.clean_text(raw)
        self.assertEqual(cleaned, "hello world this is a test 123")

    def test_preprocess_lemmatizer(self):
        tp = TextPreprocessor(method="lemmatize")
        text = "playing songs and movies in the room"
        result = tp.preprocess(text)
        self.assertNotIn("in", result.split())
        self.assertTrue(len(result) > 0)

    def test_empty_string(self):
        tp = TextPreprocessor()
        self.assertEqual(tp.preprocess(""), "")
        self.assertEqual(tp.preprocess("   "), "")
        self.assertEqual(tp.preprocess("a b to"), "")


if __name__ == "__main__":
    unittest.main()
