import os

script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(script_dir, "player.txt")

file_path = script_dir
try:
    with open(file_path, "x") as file:
        file.write("name: Alex\n")
        file.write("level: 1\n")
    print("Step 01: File created with initial data. \n")
except:
    print("Step 01: The file already exists. It was not overwritten. \n")

with open(file_path, "r") as file:
    content = file.read()

print("\nStep 02: Content of player.txt.")
print(content)

new_lines = []
with open(file_path, "r") as file:
    for line in file:
        if line.startswith("level:"):
            new_lines.append("level: 2\n")
        else:
            new_lines.append(line)

with open(file_path, "w") as file:
    file.writelines(new_lines)
print("Step 03: Level updated to 2.")

with open(file_path, "r") as file:
    content = file.read()

if "lives:" not in content:
    with open(file_path, "a") as file:
        file.write("lives: 3\n")
    print("\nStep 04: 'lives: 3' added.")
else:
    print("\nStep 04: A line with 'lives' already existed, it was not added again.")

with open(file_path, "r") as file:
    final_content = file.read()

print("\nStep 05: Final content of the file:")
print(final_content)

