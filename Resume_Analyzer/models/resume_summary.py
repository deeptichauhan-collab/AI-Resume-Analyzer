def generate_summary(skills):

    return (
        "Candidate possesses skills in "
        + ", ".join(skills[:8])
        + " and demonstrates strong technical capabilities."
    )