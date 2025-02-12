
import csv

def main():

    I_NUMBER_INDEX = 0
    NAME_INDEX = 1

    students_dict = read_dictionary("students.csv", I_NUMBER_INDEX)
    print(students_dict)
    i_number = input("Enter an I-Number to search: ")

    i_number = i_number.replace("-","")

    if not i_number.isdigit():
        print("Please enter a valid I Number")
    else:
        if len(i_number) < 9:
            print("I number should have at least 9 digits")
        elif len(i_number) >9:
            print("I number should have a maximun of 9 digits")
        else:
            if i_number in students_dict:

                value = students_dict[i_number]
                name = value[NAME_INDEX]
                print(name)
            else:
                print("No such student")
        


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

    with open(filename, mode="rt") as the_file:
        
        reader = csv.reader(the_file)
        
        next(reader)
        for row in reader:
            if len(row) != 0:
                key = row[key_column_index]
                dictionary[key] = row
    return dictionary

if __name__ == "__main__":
    main()


