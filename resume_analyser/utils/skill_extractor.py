import re

SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "react",
    "node",
    "flask",
    "django",
    "sql",
    "mongodb",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "aws",
    "docker",
    "git",
    "html",
    "css",
]


def extract_skills(text: str) -> list[str]:
    text = (text or "").lower()
    found_skills = []

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found_skills.append(skill)

    return found_skills
