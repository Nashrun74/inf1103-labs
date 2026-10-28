import json
import os


class Product:
    """Represent and manage one product."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)

    def update_stock(self, quantity):
        """Update the product's stock quantity."""
        self.__stock = int(quantity)

    def display_information(self):
        """Display this product's information."""
        print(
            f"ID: {self.__product_id}\n"
            f"Name: {self.__name}\n"
            f"Price: ${self.__price:.2f}\n"
            f"Stock: {self.__stock}"
        )

    def display_summary(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock

    def to_dict(self):
        """Convert the object to a dictionary for JSON storage."""
        return {
            "ID": self.__product_id,
            "Name": self.__name,
            "Price": self.__price,
            "Stock": self.__stock
        }


class Inventory:
    """Manage a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory\n---------------------------------")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_summary()
        print("---------------------------------")

    def get_products(self):
        return self.__products

    def load_from_data(self, data):
        """Convert loaded JSON dictionaries into Product objects."""
        self.__products = []
        for item in data:
            product = Product(
                item["ID"], item["Name"], item["Price"], item["Stock"]
            )
            self.add_product(product)


def load_inventory(inventory, filename="Lab5/inventory.json"):
    """Load product data from JSON, or use starter products if missing."""
    if os.path.exists(filename):
        print("inventory.json found.")
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            inventory.load_from_data(data)
            print("Inventory loaded successfully.")
            return
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as error:
            print(f"Could not load inventory.json: {error}")
            print("Starting with pre-filled inventory.")
    else:
        print("inventory.json not found.")
        print("Starting with pre-filled inventory.")

    inventory.load_from_data([
        {"ID": "P001", "Name": "Laptop", "Price": 1200.00, "Stock": 15},
        {"ID": "P002", "Name": "Mouse", "Price": 25.50, "Stock": 40},
        {"ID": "P003", "Name": "Keyboard", "Price": 45.00, "Stock": 25},
    ])


def save_inventory(inventory, filename="Lab5/inventory.json"):
    """Save Product objects as JSON dictionaries."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)

    data = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_integer(prompt):
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid integer.")


def get_price(prompt):
    while True:
        value = input(prompt)
        try:
            price = float(value)
            if price < 0:
                print("Price cannot be negative.")
                continue
            return price
        except ValueError:
            print("Please enter a valid price.")


def main():
    inventory = Inventory()

    print("=======================================\n"
          "INVENTORY MANAGEMENT SYSTEM\n"
          "=======================================\n")
    load_inventory(inventory)

    while True:
        print("\n--------------MENU--------------")
        print(
            "1. Display All Products\n"
            "2. Add Product\n"
            "3. Update Stock\n"
            "4. Search Product\n"
            "5. Save Inventory\n"
            "6. Exit"
        )
        print("--------------------------------")

        option = input("\nEnter option: ")
        if not option.isdigit():
            print("Please enter a valid integer.")
            continue

        option = int(option)

        if option == 1:
            inventory.display_all()

        elif option == 2:
            print("\nAdd New Product")
            product_id = input("Product ID: ").strip()
            if not product_id:
                print("Product ID cannot be empty.")
                continue
            if inventory.search_product(product_id) is not None:
                print("A product with this ID already exists.")
                continue

            name = input("Product Name: ").strip()
            if not name:
                print("Product name cannot be empty.")
                continue

            price = get_price("Price: ")
            stock = get_integer("Stock Quantity: ")
            if stock < 0:
                print("Stock quantity cannot be negative.")
                continue

            product = Product(product_id, name, price, stock)
            inventory.add_product(product)
            print("\nProduct added successfully!")

        elif option == 3:
            print("\nUpdate Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)

            if product is None:
                print("Product not found.")
                continue

            print("\nProduct Found:")
            print(f"Name: {product.get_name()}")
            print(f"Current Stock: {product.get_stock()}")
            new_stock = get_integer("\nNew Stock Quantity: ")

            if new_stock < 0:
                print("Stock quantity cannot be negative.")
                continue

            product.update_stock(new_stock)
            print("\nStock updated successfully!")

        elif option == 4:
            print("\nSearch Product")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)

            if product is None:
                print("\nProduct not found.")
            else:
                print("\nProduct Found")
                print("---------------------------------")
                product.display_information()
                print("---------------------------------")

        elif option == 5:
            try:
                save_inventory(inventory)
                print("\nInventory saved successfully to Lab5/inventory.json.")
            except OSError as error:
                print(f"Could not save inventory: {error}")

        elif option == 6:
            print("\nSaving inventory before exit...")
            try:
                save_inventory(inventory)
                print("Inventory saved successfully.")
            except OSError as error:
                print(f"Could not save inventory: {error}")
            print("\nThank you for using Inventory Management System")
            print("Program terminated.")
            break

        else:
            print("Please select a valid option.")


if __name__ == "__main__":
    main()
