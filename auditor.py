inventory = 0

while True:
    stock = input("Enter stock stock (or 'quit' to exit): ")

    if stock.lower() == "quit":
        break
        
    if not stock.isdigit():
        print("Error: Please enter a valid integer")
        continue
        

    stock = int(stock)
    inventory += stock

    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break
    else:
        print("Current stock: ", stock)

# print("Final inventory: ", inventory)