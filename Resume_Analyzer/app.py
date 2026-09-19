from flask import Flask, render_template, request
import os

from utils.pdf_reader import read_pdf

from models.skill_extractor import extract_skills
from models.ats_calculator import calculate_ats_score
from models.job_matcher import calculate_match_score
from models.suggestion_engine import generate_suggestions

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume_file = request.files["resume"]
    job_description = request.form["job_description"]

    filepath = os.path.join(
        UPLOAD_FOLDER,
        resume_file.filename
    )

    resume_file.save(filepath)

    # Read Resume
    resume_text = read_pdf(filepath)

    # Name Detection
    lines = resume_text.split("\n")

    name = "User"

    for line in lines:

        line = line.strip()

        if len(line) > 3 and len(line.split()) <= 4:

            if (
                "email" not in line.lower()
                and "phone" not in line.lower()
                and "@" not in line
            ):
                name = line
                break

    # Skills
    skills = extract_skills(resume_text)

    # Scores
    ats_score = calculate_ats_score(
        resume_text,
        job_description
        
    )

    match_score = calculate_match_score(
        resume_text,
        job_description
    )

    # Suggestions
    suggestions = generate_suggestions(
        ats_score,
        match_score,
        skills
    )

    # Strength
    if ats_score >= 80:
        strength = "Excellent"
    elif ats_score >= 60:
        strength = "Good"
    else:
        strength = "Needs Improvement"

    # Sample Questions
    questions = [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?",
        "Explain one project from your resume."
    ]

    return render_template(
        "dashboard.html",
        name=name,
        ats_score=ats_score,
        match_score=match_score,
        skills=skills,
        suggestions=suggestions,
        questions=questions,
        strength=strength
    )


if __name__ == "__main__":
    app.run(debug=True)