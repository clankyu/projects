name = input("What is your name?\n>> ")
age = int(input("What is your age?\n>> "))
height = float(input("What is your height?\n>> "))
likes_programming = None
while True:
    preference = input("Do you like programming (y/n)\n>> ").lower()
    if preference in ["yes", "y"]:
        likes_programming = True
        break
    elif preference in ["no", "n"]:
        likes_programming = False
        break
    else:
        print("Invalid input, try again")

print(type(name))
print(type(age))
print(type(height))
print(type(likes_programming))
print(f"Hello {name}, you are {age} years old, you are {height} centimeters tall, and ", end = "")
if likes_programming:
    print("you like programming.")
else:
    print("you don't like programming.")
