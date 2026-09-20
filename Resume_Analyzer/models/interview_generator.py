QUESTION_BANK = {

    "python": [
        "What are Python decorators?",
        "Difference between list and tuple?"
    ],

    "flask": [
        "What is Flask?",
        "Explain Flask routing."
    ],

    "sql": [
        "What is a JOIN?",
        "Difference between WHERE and HAVING?"
    ],

    "machine learning": [
        "What is overfitting?",
        "Difference between supervised and unsupervised learning?"
    ]
}


def generate_questions(skills):

    questions = []

    for skill in skills:

        if skill in QUESTION_BANK:

            questions.extend(
                QUESTION_BANK[skill]
            )

    return questions[:10]