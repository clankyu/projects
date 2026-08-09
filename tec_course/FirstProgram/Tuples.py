personal_data = ("John", 18, "Monterrey", "Student", True)
print("Personal data: ", personal_data)
print(personal_data[0])
print(personal_data[-1])

if "Student" in personal_data:
    print("The person is a student")

print("Looping through tuple:")
for item in personal_data:
    print("-", item)

print("Number of elements: ", len(personal_data))

other = ("Python", "Github")
combined = personal_data + other
print("Combined tuple:", combined)