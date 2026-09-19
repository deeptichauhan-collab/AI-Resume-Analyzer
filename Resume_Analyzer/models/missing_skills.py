def get_missing_skills(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())

    missing = jd_words - resume_words

    return list(missing)[:10]