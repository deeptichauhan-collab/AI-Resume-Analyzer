def calculate_ats_score(
        resume_text,
        job_description):

    score = 60

    jd_words = job_description.lower().split()

    for word in jd_words:
        if word in resume_text.lower():
            score += 1

    return min(score, 100)