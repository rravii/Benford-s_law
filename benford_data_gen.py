import csv
import random

benford_data = []
for i in range(15000):
    first_digit = random.randint(1, 9)
    remaining_digits = random.randint(0, 999)
    number = int(str(first_digit) + str(remaining_digits).zfill(3))
    benford_data .append(number)

with open('benford_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['List'])
    for number in benford_data :
        writer.writerow([number])

