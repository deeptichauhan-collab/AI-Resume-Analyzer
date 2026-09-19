import re

# Skills Database
SKILLS_DB = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "mongodb",
    "flask",
    "django",
    "react",
    "nodejs",
    "express",
    "machine learning",
    "deep learning",
    "data science",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "linux",
    "bootstrap"
]


def extract_skills(text):
    """
    Extract matching skills from resume text
    """

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))