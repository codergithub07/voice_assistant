"""
Tests for Jarvis configuration module in src/jarvis/config.py.
"""

import unittest
from jarvis.config import (
    SAMPLE_RATE,
    BLOCK_SIZE,
    CHANNELS,
    DTYPE,
    CONFIDENCE_THRESHOLD,
    DEFAULT_VOSK_MODEL,
)


class TestConfig(unittest.TestCase):

    def test_default_config(self):
        self.assertEqual(SAMPLE_RATE, 16000)
        self.assertEqual(BLOCK_SIZE, 8000)
        self.assertEqual(CHANNELS, 1)
        self.assertEqual(DTYPE, "int16")
        self.assertEqual(CONFIDENCE_THRESHOLD, 0.55)
        self.assertTrue(str(DEFAULT_VOSK_MODEL).endswith("vosk-model-small-en-us-0.15"))


if __name__ == "__main__":
    unittest.main()
