inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock stock (or 'quit' to exit): ")

    if stock.lower() == "quit":
        print("Total Units Processed: ", inventory)
        print("Number of Failed/Rejected Entries: ", failed_entries)
        break
        
    if not stock.isdigit():
        print("Error: Please enter a valid integer")
        failed_entries += 1
        continue
        

    stock = int(stock)
    inventory += stock

    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        failed_entries += 1
        break
    else:
        print("Current stock: ", stock)