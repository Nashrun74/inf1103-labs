inventory = 0

while True:
    quantity = input("Enter stock quantity (or 'quit' to exit): ")

    if quantity.lower() == "quit":
        break

    print("Stock quantity entered:", quantity)