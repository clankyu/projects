wednesday = input("Will you attend on Wednesday?\n")
number_tickets = int(input("How many tickets would you like to buy?\n"))
payment_method = input("Will you pay in cash? (y/n)\n")
individual_price = 200

if wednesday.lower() in ["yes", "y"]:
    individual_price *= 0.7

total = individual_price * number_tickets
if number_tickets > 3:
    total *= 0.9

print(f"Individual price is: ${round(individual_price, 2)}")
print(f"The total with discounts is: ${round(total, 2)}")

if payment_method.lower() in ["yes", "y"] and total > 500:
    print("Congratulations! You can have a free coupon for your next visit :)")