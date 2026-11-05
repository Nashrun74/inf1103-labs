import json
import os
from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style contract for products that can be shipped."""

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class Product(ABC):
    """Abstract base class shared by physical and digital products."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = str(product_id)
        self.__name = str(name)
        self.__price = float(price)
        self.__stock = int(stock)

    def update_stock(self, quantity):
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id}\n"
            f"Name: {self.__name}\n"
            f"Price: ${self.__price:.2f}\n"
            f"Stock: {self.__stock}"
        )

    def display_summary(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_stock(self):
        return self.__stock

    def get_price(self):
        return self.__price

    @abstractmethod
    def get_fulfilment_info(self):
        """Return how this product is fulfilled."""
        pass

    @abstractmethod
    def to_dict(self):
        """Return all product data, including its type, for JSON."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)
        if self.__weight < 0:
            raise ValueError("Weight cannot be negative.")

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight:.2f} kg")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        # Demonstration rule: $2.00 base + $1.50 per kilogram.
        return 2.00 + (1.50 * self.__weight)

    def to_dict(self):
        return {
            "type": "physical",
            "ID": self.get_product_id(),
            "Name": self.get_name(),
            "Price": self.get_price(),
            "Stock": self.get_stock(),
            "Weight": self.__weight
        }


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)
        if self.__download_size < 0:
            raise ValueError("Download size cannot be negative.")

    def display_information(self):
        super().display_information()
        print(f"Download size: {self.__download_size:.2f} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self):
        return "Delivered digitally."

    def to_dict(self):
        return {
            "type": "digital",
            "ID": self.get_product_id(),
            "Name": self.get_name(),
            "Price": self.get_price(),
            "Stock": self.get_stock(),
            "DownloadSize": self.__download_size
        }


class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            raise ValueError("A product with this ID already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id() == str(product_id):
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
        products = []
        for item in data:
            kind = item.get("type", "physical")
            common = (item["ID"], item["Name"], item["Price"], item["Stock"])
            if kind == "physical":
                product = PhysicalProduct(*common, item["Weight"])
            elif kind == "digital":
                product = DigitalProduct(*common, item["DownloadSize"])
            else:
                raise ValueError(f"Unknown product type: {kind}")
            products.append(product)
        self.__products = products


def load_inventory(inventory, filename="Lab7/inventory.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                inventory.load_from_data(json.load(file))
            print(f"Inventory loaded from {filename}.")
            return
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as error:
            print(f"Could not load {filename}: {error}")
            print("Starting with sample inventory.")
    else:
        print(f"{filename} not found. Starting with sample inventory.")

    inventory.load_from_data([
        {"type": "physical", "ID": "P001", "Name": "Laptop", "Price": 1200.00, "Stock": 15, "Weight": 2.4},
        {"type": "digital", "ID": "D001", "Name": "Photo Editor", "Price": 49.90, "Stock": 100, "DownloadSize": 850}
    ])


def save_inventory(inventory, filename="Lab7/inventory.json"):
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump([p.to_dict() for p in inventory.get_products()], file, indent=4)


def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def get_nonnegative_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def main():
    inventory = Inventory()
    print("=======================================\nINVENTORY MANAGEMENT SYSTEM\n=======================================")
    load_inventory(inventory)

    while True:
        print("\n1. Display All Products\n2. Add Product\n3. Update Stock\n4. Search Product\n5. Save Inventory\n6. Exit")
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            if not product_id or not name:
                print("ID and name cannot be empty.")
                continue
            if inventory.search_product(product_id):
                print("A product with this ID already exists.")
                continue
            price = get_nonnegative_float("Price: $")
            stock = get_integer("Stock quantity: ")
            if stock < 0:
                print("Stock quantity cannot be negative.")
                continue
            kind = input("Product type (physical/digital): ").strip().lower()
            try:
                if kind == "physical":
                    extra = get_nonnegative_float("Weight (kg): ")
                    product = PhysicalProduct(product_id, name, price, stock, extra)
                elif kind == "digital":
                    extra = get_nonnegative_float("Download size (MB): ")
                    product = DigitalProduct(product_id, name, price, stock, extra)
                else:
                    print("Please enter physical or digital.")
                    continue
                inventory.add_product(product)
                print("Product added successfully.")
            except ValueError as error:
                print(error)
        elif option == "3":
            product = inventory.search_product(input("Product ID: ").strip())
            if product is None:
                print("Product not found.")
                continue
            print(f"{product.get_name()} | Current stock: {product.get_stock()}")
            new_stock = get_integer("New stock quantity: ")
            if new_stock < 0:
                print("Stock quantity cannot be negative.")
            else:
                product.update_stock(new_stock)
                print("Stock updated successfully.")
        elif option == "4":
            product = inventory.search_product(input("Product ID: ").strip())
            if product is None:
                print("Product not found.")
            else:
                product.display_information()
        elif option == "5":
            try:
                save_inventory(inventory)
                print("Inventory saved successfully.")
            except OSError as error:
                print(f"Could not save inventory: {error}")
        elif option == "6":
            try:
                save_inventory(inventory)
                print("Inventory saved.")
            except OSError as error:
                print(f"Could not save inventory: {error}")
            print("Thank you for using Inventory Management System.")
            break
        else:
            print("Please select a valid option.")


if __name__ == "__main__":
    main()
