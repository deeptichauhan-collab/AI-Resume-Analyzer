def calculate_match_score(resume_text, job_description):
    """
    Calculate resume-job match score
    """

    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())

    if len(jd_words) == 0:
        return 0

    matched_words = resume_words.intersection(jd_words)

    score = (len(matched_words) / len(jd_words)) * 100

    return round(score, 2)