import os
from datetime import datetime

os.system('cls' if os.name == 'nt' else clear)
subtotal = None

while subtotal != 0:
    subtotal = float(input('What is your subtotal? '))
    if subtotal == 0:
        break
    else:
        is_tuesday = datetime.today().weekday() in (2,3)
        subtotal_discount = None
        get_discount = None
        get_discount_bool = None
        if subtotal >= 50 and is_tuesday == True:
            subtotal_discount = subtotal - (subtotal * 0.10)
        else:
            get_discount_bool = True
            get_discount = 50 - subtotal
        print(f'Your subtotal is {subtotal}{" taking the discount the total is " if subtotal >= 50 and is_tuesday == True else ""}{subtotal_discount if subtotal >= 50 and is_tuesday == True else ""}')
        if get_discount_bool:
            print(f'You need to add {get_discount} to get the discount')
