# If the user wants to buy tires, we ask for the phone number and store it in the file
# Imported os so that each time the code runs, it cleans the terminal

import math
import os
from datetime import datetime

os.system('cls' if os.name == "nt" else "clear")

width = float(input('Enter the width of the tire in mm (ex 205): '))

radio = float(input('Enter the aspect ratio of the tire (ex 60): '))

diameter = float(input('Enter the diameter of the wheel in inches (ex 15): '))

volume_value = (math.pi * (width ** 2) * radio * ((width * radio) + (2540 * diameter)))/(10000000000)

print(f'The approximate volume is {volume_value:.2f} liters')

buy = "Y"
phone = None

while True:
    buy = input('Do you want to buy tires of the dimensions provided? (Y/N)').upper()
    if buy == "Y":
        phone = int(input('Whats your phone number? '))
        break
    elif buy == "N":
        print("Thank you for your time")
        break
    else:
        print('Please provide a valid value')


time = datetime.now().date()

with open("volumes.txt", mode="at") as volume:
    print(f'{time}, {width}, {radio}, {diameter}, {volume_value:.2f}, {phone}', file=volume)


