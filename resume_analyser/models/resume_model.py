"""Resume model definitions."""


class ResumeModel:
    """Placeholder resume model."""

    def __init__(self):
        self.name = "ResumeModel"

    def predict(self, text: str) -> dict:
        """Return a placeholder prediction for a resume."""
        return {"text_length": len(text), "predicted_labels": []}
