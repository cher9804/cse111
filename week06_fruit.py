def main():
  # Create and print a list named fruit.
  fruit_list = ["pear", "banana", "apple", "mango"]
  print(f"original: {fruit_list}")
  fruit_list.reverse()
  print(f"reversed: {fruit_list}")
  fruit_list.append("Orange")
  print(f"Orange: {fruit_list}")
  index = fruit_list.index("apple")
  fruit_list.insert(index, "cherry")
  print(f"Insert Cherry: {fruit_list}")
  fruit_list.remove("banana")
  print(f"No banana: {fruit_list}")
  fruit_list.pop()
  print(f"No orange: {fruit_list}")
  fruit_list.sort()
  print(f"Sort: {fruit_list}")
  fruit_list.clear()
  print(f"Clear: {fruit_list}")




main()