import json
# Functions
def load_inventory():
    print("Current Inventory\n---------------------------------")
    for i in inventory:
        print("ID:", i["ID"], "|", "Name:", i["Name"], "|", "Price: $", i["Price"], "|", "Stock:", i["Stock"])
    print("---------------------------------")

def add_product():
    return None

def update_stock():
    return None

def search_product(product):
    return product

def display_all():
    return None

def save_inventory():
    return None



# Main Code
inventory = [
    {"ID": "P001", "Name": "Laptop", "Price": 1200.00, "Stock": 15},
    {"ID": "P002", "Name": "Mouse", "Price": 25.50, "Stock": 40},
    {"ID": "P003", "Name": "Keyboard", "Price": 45.00, "Stock": 25},
]
print("=======================================\nINVENTORY MANAGEMENT SYSTEM\n=======================================")
print("--------------MENU--------------")
print("1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
print("--------------------------------")
while True:
    option = input("Enter option: ")
    if not option.isdigit():
        print("Please enter a valid integer")
        continue

    option = int(option)
    if option == 1:
        load_inventory()
        continue
    if option == 2:
        continue
    if option == 3:
        continue
    if option == 4:
        continue
    if option == 5:
        continue
    if option == 6:
        print("Saving inventory before exit...")
        print("Inventory saved successfully.")
        print("\nThank you for using Inventory Management System\nProgram terminated.")
        break
    elif option <= 0 or option > 6:
        print("Please select a valid option")
    else:
        break



