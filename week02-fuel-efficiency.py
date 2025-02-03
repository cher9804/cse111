import os

os.system('cls' if os.name == 'nt' else 'clear')

def main():
    start_odo = float(input('Enter the starting odometer value in miles: '))
    end_odo = float(input('Enter the ending odometer value in miles: '))
    fuel = float(input('Enter the ful in gallons: '))
    mpg = miles_per_gallon(start_odo, end_odo, fuel)
    lp100k = lp100k_from_mpg(mpg)
    print(f'{mpg:.1f} miles per gallon')
    print(f'{lp100k:.2f} liters per 100 kilometers')

def miles_per_gallon(start, end, fuel):
    mpg = (end-start)/fuel
    return mpg

def lp100k_from_mpg(mpg):
    lp100k = 235.215/mpg
    return lp100k

main()

