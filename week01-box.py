import os
import math

os.system('cls' if os.name == 'nt' else 'clear')

items = int(input('How many manufactured items you have? '))
box = int(input('How many items the user will pack per box? '))

boxes_need = math.ceil(items / box)

boxes_need_mine = items/box
if (boxes_need_mine % 10) >= 6:
    boxes_need_mine += 1


print(f'You will need {boxes_need} {"box" if boxes_need==1 else "boxes"}')

print(f'You will need {boxes_need_mine:.0f} {"box" if boxes_need==1 else "boxes"}')

