import json
import os
# Functions
def display_all():
    print("\nCurrent Inventory\n---------------------------------")
    for i in inventory:
        print(
            f"ID: {i["ID"]} | "
            f"Name: {i["Name"]} | "
            f"Price: ${i["Price"]:.2f} | "
            f"Stock: {i["Stock"]}"
        )
    print("---------------------------------")\

def add_product():
    print("\nAdd New Product")
    
    id = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    new_product = {
        "ID": id,
        "Name": name,
        "Price": price,
        "Stock": stock
    }

    inventory.append(new_product)
    print("\nProduct added successfully!")

def update_stock():
    print("\nUpdate Stock")
    id = input("Enter Product ID: ")

    for i in inventory:
        if i["ID"] == id:
            print("\nProduct Found: ")
            print(f"Name: {i["Name"]}")
            print(f"Current Stock: {i["Stock"]}")

            new_stock = int(input("\nNew Stock Quantity: "))

            i["Stock"] = new_stock

            print("\nStock updated successfully!")
            return

    print("Product not found.")

def search_product():
    print("\nSearch Product")

    id = input("Enter Product ID: ")
    for i in inventory:
        if i["ID"] == id:
            print("\nProduct Found")
            print("---------------------------------")
            print(
                f"ID: {i["ID"]}\n"
                f"Name: {i["Name"]}\n"
                f"Price: ${i["Price"]:.2f}\n"
                f"Stock: {i["Stock"]}"
            )
            print("---------------------------------")
            return

    print("\nProduct not found.")

def load_inventory():
    global inventory

    if os.path.exists("Lab5/inventory.json"):
        print("inventory.json found.")

        with open("Lab5/inventory.json", "r") as file:
            inventory = json.load(file)

        print("Inventory loaded successfully.")

    else:
        print("inventory.json not found.")
        print("Starting with pre-filled inventory")
        inventory = [
            {"ID": "P001", "Name": "Laptop", "Price": 1200.00, "Stock": 15},
            {"ID": "P002", "Name": "Mouse", "Price": 25.50, "Stock": 40},
            {"ID": "P003", "Name": "Keyboard", "Price": 45.00, "Stock": 25},
        ]

def save_inventory():
    with open("Lab5/inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)


# Main Code

print("=======================================\nINVENTORY MANAGEMENT SYSTEM\n=======================================\n")
load_inventory()
print("\n--------------MENU--------------")
print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
print("--------------------------------\n")
while True:
    option = input("\nEnter option: ")
    if not option.isdigit():
        print("Please enter a valid integer")
        continue

    option = int(option)
    if option == 1:
        display_all()
        continue
    if option == 2:
        add_product()
        continue
    if option == 3:
        update_stock()
        continue
    if option == 4:
        search_product()
        continue
    if option == 5:
        save_inventory()
        print("\nSaving Inventory...")
        print("Inventory saved successfully to inventory.json.")
        continue
    if option == 6:
        print("\nSaving inventory before exit...")
        save_inventory()
        print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System\nProgram terminated.")
        break
    elif option <= 0 or option > 6:
        print("Please select a valid option")
    else:
        print("Logging off...")
        break



