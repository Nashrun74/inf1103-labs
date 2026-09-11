inventory = 0

while True:
    quantity = input("Enter stock quantity (or 'quit' to exit): ")

    if quantity.lower() == "quit":
        break
        
    if not quantity.isdigit():
        print("Error: Please enter a valid integer")
        continue

    quantity = int(quantity)
    print("Stock quantity entered: ", quantity)