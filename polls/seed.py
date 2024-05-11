from polls.models import db, Question, Choice


def create_seed_data():
    print("Seeding...")
    # Sample questions
    questions_data = [
        {
            "question_text": "What is your favorite color?",
            "choices": ["Red", "Blue", "Green"],
        },
        {
            "question_text": "What is your favorite animal?",
            "choices": ["Dog", "Cat", "Bird"],
        },
        {
            "question_text": "Which programming language do you prefer?",
            "choices": ["Python", "JavaScript", "Java", "C++"],
        },
        {
            "question_text": "What is your favorite movie genre?",
            "choices": ["Action", "Comedy", "Drama", "Sci-Fi"],
        },
    ]

    # Create questions and choices
    for question_data in questions_data:
        question = Question(question_text=question_data["question_text"])
        db.session.add(question)
        db.session.commit()

        for choice_text in question_data["choices"]:
            choice = Choice(question_id=question.id, choice_text=choice_text)
            db.session.add(choice)

    db.session.commit()
