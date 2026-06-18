"""Unit tests for the resume model."""

import unittest

from resume_analyser.models.resume_model import ResumeModel


class TestResumeModel(unittest.TestCase):
    def test_predict_returns_dict(self):
        model = ResumeModel()
        result = model.predict("Sample resume text")

        self.assertIsInstance(result, dict)
        self.assertIn("text_length", result)
        self.assertEqual(result["text_length"], len("Sample resume text"))


if __name__ == "__main__":
    unittest.main()
