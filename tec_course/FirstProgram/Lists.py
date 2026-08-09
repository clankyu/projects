names = ["Ann", "Louis", "Karla", "Peter"]
print("complete lists: ", names)

print("first name: ", names[0])
print("second name: ", names[1])
names[1] = "Charles"
names.append("Mary")
print("New names list: ", names)
if "Mary" in names:
    print("Mary is in the list.")
else:
    print("Mary is not in the list")

names.sort()
print("Looping through the list: ")
for name in names:
    print(name)

print("List size: ", len(names))

names.clear()
print("Empty list: ", names)

names = ["Ann", "Louis", "Karla", "Peter"]
sliced_names = names[1:2]

list_of_lists = [names, names]
print("Value: ", list_of_lists[0][1])
