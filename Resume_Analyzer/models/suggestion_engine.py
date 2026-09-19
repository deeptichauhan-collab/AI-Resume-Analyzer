def generate_suggestions(
        ats_score,
        match_score,
        skills):

    suggestions = []

    if ats_score < 60:
        suggestions.append(
            "Add more technical skills relevant to your target role."
        )

    if match_score < 70:
        suggestions.append(
            "Customize your resume according to the job description."
        )

    if "github" not in skills:
        suggestions.append(
            "Add your GitHub profile and projects."
        )

    if "docker" not in skills:
        suggestions.append(
            "Learning Docker can improve your technical profile."
        )

    if "aws" not in skills:
        suggestions.append(
            "Cloud skills such as AWS are highly valued."
        )

    if len(skills) < 5:
        suggestions.append(
            "Include more technologies and tools you have worked with."
        )

    if not suggestions:
        suggestions.append(
            "Your resume looks strong and ATS friendly."
        )

    return suggestions