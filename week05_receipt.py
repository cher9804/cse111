import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
# Needed to install dateutil "pip install python-dateutil" used this to install it 



def main():
    try:
        PRODUCT_KEY_INDEX = 0
        PRODUCT_NAME_INDEX = 1
        PRODUCT_PRICE_INDEX = 2
        REQUEST_QUANTITY_INDEX = 1
        REQUEST_PRODUCT_INDEX = 0

        products_dict = read_dictionary("products.csv", PRODUCT_KEY_INDEX)
        # print("All products")
        # print(products_dict)
        print("Inkom Emporium")
        print(f"Name \tQuantity \tPrice \t Type Payment \t Total Product".expandtabs(20))


        with open("request.csv", mode="rt") as request:
            reader = csv.reader(request)
            next(reader)
            subtotal = 0
            quantity_products = 0
            for row in reader:
                product = row[REQUEST_PRODUCT_INDEX]
                quantity = int(row[REQUEST_QUANTITY_INDEX])
                if product in products_dict:                    
                    items_in_dict = products_dict[product]
                    price = float(items_in_dict[PRODUCT_PRICE_INDEX])
                    name = items_in_dict[PRODUCT_NAME_INDEX]
                    if product == "D083":
                        full_price_items = quantity // 2 # 5 // 2  # Result: 2
                        discounted_items = quantity - full_price_items
                        discounted_price = price / 2
                        total_product_price = (full_price_items * price) + (discounted_items * discounted_price)
                    else:
                        total_product_price = price * quantity


                    print(f"{name.capitalize()}: \t{quantity} \t{price} \t({'Discounted' if product == 'D083' else 'Full Price'}) \t {total_product_price}".expandtabs(20))
                    quantity_products += quantity
                    subtotal += total_product_price
                else:
                    raise KeyError(f"Unkownd product ID: {product}")

            print(f"Number of Items: {quantity_products}")

            print(f"Subtotal: {subtotal:.2f}")
            SALES_TAX_RATE = 0.06
            sales_tax = subtotal * SALES_TAX_RATE
            total = subtotal + sales_tax
            print(f"Sales Tax: {sales_tax:.2f}")
            print(f"Total: {total:.2f}")
            print("Thank you for shopping at the Inkom Empotium")
            now = datetime.now()
            formatted_date = now.strftime("%a %b %e %H:%M:%S %Y")
            print(f"{formatted_date}")
            next_year = now.year + 1
            target_date = datetime(next_year, 1, 1)
            days_until_promo = (target_date - now).days
            # using the datetime module
            print(f"There are {days_until_promo} days until our New Years Sale which begins on (Jan 1)")
            difference = relativedelta(target_date, now) #relativedelta(months=+10, days=+20, hours=+1, minutes=+51, seconds=+23, microseconds=+90370)
            months_until_jan_1 = difference.months
            days_until_jan_1 = difference.days
            print(f"It means that there are {months_until_jan_1} months and {days_until_jan_1} days for the Sale.")
            thirty_days = now.day + 30
            thirty_days = now.strftime("%a %b %e %Y")
            print(f"Please return by {thirty_days} at 9:00 PM (30 days from today)")
            

    except KeyError as key_error:
        print(f"Error: unkown product ID in the request.csv file {key_error}")
    except FileNotFoundError as no_file:
        print(f"Error: {no_file}. Please ensure the file '{no_file.filename}' exists.")
    except PermissionError as permission_error:
        print(f"Error: {permission_error}. Please check file permissions.")
    except IndexError as index_error:
        print(f"Error: {index_error}. Please ensure the file has the correct columns and data in it")
    
        






        


def read_dictionary(filename, key_column_index):
    """Read the contents of a CSV file into a compound
  dictionary and return the dictionary.
  Parameters
      filename: the name of the CSV file to read.
      key_column_index: the index of the column
          to use as the keys in the dictionary.
  Return: a compound dictionary that contains
      the contents of the CSV file.
    """
    dictionary = {}

    with open(filename, mode="rt") as csv_file:

        reader = csv.reader(csv_file)

        next(reader)

        for row in reader:
            if len(row) !=0:
                key = row[key_column_index]
                dictionary[key] = row
    
    return dictionary

if __name__ == "__main__":
    main()