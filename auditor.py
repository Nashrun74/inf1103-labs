inventory = 0

while True:
    quantity = input("Enter stock quantity (or 'quit' to exit): ")

    if quantity.lower() == "quit":
        break

    try:
        quantity = int(quantity)
        print("Stock quantity entered: ", quantity)
    except ValueError:
        print("Error: Please enter an integer")