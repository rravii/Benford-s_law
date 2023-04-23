import csv
import random

non_benford_data = []
for i in range(15000):
    # Generate a random number between 1.0 and 9999.0
    number = random.uniform(1.0, 9999.0)

    # Modify the first digit of the number
    first_digit = int(str(number)[0])
    if first_digit in [1, 2, 3, 4, 5, 6]:
        # Shift the first digit up by one
        first_digit += 1
    else:
        # Shift the first digit down by one
        first_digit -= 1

    # Replace the first digit with the modified digit
    modified_number = float(str(first_digit) + str(number)[1:])

    # Add the modified number to the list
    non_benford_data.append(modified_number)

with open('non_benford_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['List'])
    for number in non_benford_data:
        writer.writerow([number])