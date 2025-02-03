"""
When you physically exercise to strengthen your heart, you
should maintain your heart rate within a range for at least 20
minutes. To find that range, subtract your age from 220. This
difference is your maximum heart rate per minute. Your heart
simply will not beat faster than this maximum (220 - age).
When exercising to strengthen your heart, you should keep your
heart rate between 65% and 85% of your heart’s maximum rate.
"""

import os
os.system("cls" if os.name == "nt" else "clear")

age = int(input("What is your age? "))

max_heart = 220 - age
hr_65 = max_heart * 0.65
hr_85 = max_heart * 0.85

print(f'When you exersice to strengthen your heart, you should keep your heart rate between {hr_65:.0f} and {hr_85:.0f}')