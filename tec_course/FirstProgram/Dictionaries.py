student = {
    "name" : "Mary",
    "age" : 15,
    "id" : "A01179321",
    "gpa" : 5.0
}

print("Student's name: ", student["name"])

student["gpa"] = 4.5
student["major"] = "Engineering"

del student["age"]
print("Keys:", student.keys())
print("Values:", student.values())

print("Is 'name' in the dictionary? ", "name" in student)
print("\nStudent data:")
for key, value in student.items():
    print(f"{key}: {value}")

course = {
    "name" : "Advanced Programming",
    "code" : "PROG-101",
    "credits" : 4,
    "students" : [student]
}

new_student = {
    "name" : "John",
    "age" : 17,
    "id" : "A01234568",
    "gpa" : 8.7
}

missing_age_student = {
    "name" : "Ann",
    "id" : "A01234569",
    "gpa" : 9.0
}

course["students"].append(missing_age_student)

for student in course["students"]:
    if student["id"] == "A01234568":
        print("Name with ID A01234568: ", student["name"])

print("\nNames of the student in the course:")
for student in course["students"]:
    print(student["name"])

total_gpa = (
    sum(student["gpa"] for student in course["students"]) / len(course["students"])
)

print("Total Gpa of the students: ", total_gpa)

print("\nTrying to get the age of each student:")
for student in course["students"]:
    age = student.get("age", "Age not recorded")
    print(f"Age of {student["name"]}: {age}")

course["students"] = [
    student for student in course["students"]
    if student["id"] != "A01234568"
]

print("\nUpdated course:")
for key, value in course.items():
    print(f"{key}: {value}")