from flask import Flask, render_template, request, send_file, session
import os
from reportlab.pdfgen import canvas

from utils.pdf_reader import read_pdf

from models.skill_extractor import extract_skills
from models.ats_calculator import calculate_ats_score
from models.job_matcher import calculate_match_score
from models.suggestion_engine import generate_suggestions

app = Flask(__name__)
app.secret_key = "resume_ai_secret"

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

    # ==========================
    # Auto Name Detection
    # ==========================

    lines = resume_text.split("\n")
    name = "User"

    for line in lines:

        line = line.strip()

        if (
            len(line) > 3
            and len(line.split()) <= 4
            and "@" not in line
            and "email" not in line.lower()
            and "phone" not in line.lower()
        ):
            name = line
            break

    # ==========================
    # Skills
    # ==========================

    skills = extract_skills(resume_text)
    summary = f"""
    Candidate possesses skills in {', '.join(skills)}
    and demonstrates strong technical capabilities.
    """

    # ==========================
    # Scores
    # ==========================

    ats_score = calculate_ats_score(
        resume_text,
        job_description
    )

    match_score = calculate_match_score(
        resume_text,
        job_description
    )

    # ==========================
    # Suggestions
    # ==========================

    suggestions = generate_suggestions(
        ats_score,
        match_score,
        skills
    )

    # ==========================
    # Missing Skills
    # ==========================

    required_skills = [
        "python",
        "flask",
        "html",
        "css",
        "javascript",
        "mysql",
        "git",
        "docker",
        "aws"
    ]

    missing_skills = []

    resume_skills_lower = [
        skill.lower() for skill in skills
    ]

    for skill in required_skills:

        if skill not in resume_skills_lower:
            missing_skills.append(skill.title())

    # ==========================
    # Professional Summary
    # ==========================

    if len(skills) > 0:

        professional_summary = (
            f"Candidate possesses expertise in "
            f"{', '.join(skills[:10])}. "
            f"The resume demonstrates strong technical "
            f"skills and project experience."
        )

    else:

        professional_summary = (
            "Resume uploaded successfully. "
            "Add more technical skills and projects "
            "to improve profile strength."
        )

    # ==========================
    # Strength
    # ==========================

    if ats_score >= 80:
        strength = "Excellent"

    elif ats_score >= 60:
        strength = "Good"

    else:
        strength = "Needs Improvement"

    # ==========================
    # Interview Questions
    # ==========================

    questions = [
        "Tell me about yourself.",
        "Why should we hire you?",
        "Explain one project from your resume.",
        "What are your strengths and weaknesses?",
        "How do you solve technical challenges?"
    ]

    # ==========================
    # Save for PDF Report
    # ==========================

    session["ats_score"] = ats_score
    session["match_score"] = match_score
    session["name"] = name

    return render_template(
        "dashboard.html",

        name=name,

        ats_score=ats_score,

        match_score=match_score,

        skills=skills,

        suggestions=suggestions,

        missing_skills=missing_skills,

        professional_summary=professional_summary,

        questions=questions,

        strength=strength ,
        summary=summary
    )


@app.route("/download_report")
def download_report():

    pdf_file = "Resume_Report.pdf"

    c = canvas.Canvas(pdf_file)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(
        100,
        800,
        "AI Resume Analysis Report"
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        100,
        760,
        f"Candidate: {session.get('name','User')}"
    )

    c.drawString(
        100,
        730,
        f"ATS Score: {session.get('ats_score',0)}%"
    )

    c.drawString(
        100,
        700,
        f"Job Match Score: {session.get('match_score',0)}%"
    )

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)