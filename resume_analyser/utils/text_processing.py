"""Text processing utilities for the resume analyzer."""

import os
import re

import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

KNOWN_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "data science",
    "natural language processing",
    "nlp",
    "deep learning",
    "statistics",
    "excel",
    "tableau",
    "power bi",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "communication",
    "project management",
    "leadership",
    "cloud",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "presentation",
]


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    text = text or ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using pdfplumber."""
    if not os.path.exists(file_path):
        return ""

    extracted_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)

    return clean_text("\n".join(extracted_text))


def extract_skills(text: str, skill_set: list[str] | None = None) -> list[str]:
    """Detect known skills in text."""
    text = clean_text(text).lower()
    skill_set = skill_set or KNOWN_SKILLS
    found = []

    for skill in skill_set:
        normalized = skill.lower()
        pattern = r"\b" + re.escape(normalized) + r"\b"
        if re.search(pattern, text):
            found.append(skill)

    return sorted(set(found))


def compute_similarity(text_a: str, text_b: str) -> float:
    """Compute cosine similarity between two pieces of text."""
    text_a = clean_text(text_a)
    text_b = clean_text(text_b)
    if not text_a or not text_b:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([text_a, text_b])
    similarity_matrix = cosine_similarity(vectors[0:1], vectors[1:2])
    return float(similarity_matrix[0][0])


def score_resume(resume_text: str, job_description: str, skill_set: list[str] | None = None) -> dict:
    """Score a resume against a job description."""
    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)
    skill_set = skill_set or KNOWN_SKILLS

    resume_skills = extract_skills(resume_text, skill_set)
    job_skills = extract_skills(job_description, skill_set)
    matched_skills = sorted(set(resume_skills).intersection(job_skills))

    skill_score = 0.0
    if job_skills:
        skill_score = len(matched_skills) / len(set(job_skills))

    semantic_similarity = compute_similarity(resume_text, job_description)
    overall_score = round((skill_score * 0.65 + semantic_similarity * 0.35) * 100, 2)

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "skill_score": round(skill_score * 100, 2),
        "semantic_similarity": round(semantic_similarity * 100, 2),
        "overall_score": overall_score,
    }
