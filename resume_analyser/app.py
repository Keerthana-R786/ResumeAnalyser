from flask import Flask, request, render_template
import os

from utils.resume_parser import extract_text
from utils.skill_extractor import extract_skills
from utils.text_processing import score_resume

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("resume")
    if not file:
        return {"message": "No resume file provided"}, 400

    if file.filename == "":
        return {"message": "Empty filename received"}, 400

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    resume_text = extract_text(file_path)
    if resume_text == "Unsupported file format":
        return {"message": "Unsupported file type. Please upload PDF or DOCX."}, 400

    if not resume_text:
        return {"message": "Unable to extract text from resume"}, 500

    skills = extract_skills(resume_text)

    job_description = request.form.get(
        "job_description",
        "We are seeking a data scientist with strong experience in Python, SQL, machine learning, and data analysis."
    )

    score = score_resume(resume_text, job_description)

    return {
        "message": "Resume analyzed successfully",
        "filename": file.filename,
        "skills": skills,
        "skill_count": len(skills),
        "text_preview": resume_text[:500],
        "job_description": job_description,
        **score
    }

if __name__ == "__main__":
    app.run(debug=True)
