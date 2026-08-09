import pandas as pan

questions = pan.read_csv("questionare.csv")
# do something bla bla bla
questions = [
    "Question 1 (placeholder)",
    "Question 2 (placeholder)",
    "Question 3 (placeholder)",
    "Question 4 (placeholder)",
    "Question 5 (placeholder)"
]

answers = []

question_number = 0
for q in questions:
    answers.insert(0, f"{input(questions[question_number])}\n >> ")
    question_number += 1

print("Please confirm your answers:")

question_number = 0
confirm = False
while confirm == False:
    for q in questions:
        print(f"{questions[question_number]}")
        print(f"Answer: {answers[question_number]}\n")
        question_number += 1

    if input("Do you confirm? (y/n)").lower() in ["y", "yes"]:
        confirm = True
    else:
        question_number = 0

print("Result (placeholder)")

