import json
import os
from supplier import Supplier
from product import Product
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from product_loader import load_products
from input_helpers import get_positive_float
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount

INVENTORY_FILE: str = "inventory.json"

def sample_inventory() -> Inventory:
    inventory: Inventory = Inventory()
    supplier1: Supplier = Supplier("S001", "Tech Supplies Pte Ltd", "sales@tech.example")
    supplier2: Supplier = Supplier("S002", "Digital World Pte Ltd", "help@digital.example")
    inventory.add_product(ProductFactory.create("physical", "P001", "Laptop", 1200.0, 15, supplier1, 2.5))
    inventory.add_product(ProductFactory.create("physical", "P002", "Mouse", 25.5, 40, supplier1, 0.15))
    inventory.add_product(ProductFactory.create("digital", "D001", "Antivirus Software", 45.0, 100, supplier2, 250.0))
    return inventory

def product_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Product:
    # Reuse the Supplier object for products with the same SupplierID.
    sd: dict = data["Supplier"]
    sid: str = sd["SupplierID"]
    if sid not in suppliers:
        suppliers[sid] = Supplier(sid, sd["Name"], sd["ContactEmail"])
    supplier: Supplier = suppliers[sid]
    # Unknown types raise ValueError inside the factory.
    kind: str = data["type"]
    extra: float = 1.0
    if kind == "physical":
        extra = float(data["Weight"])
    elif kind == "digital":
        extra = float(data["DownloadSize"])
    return ProductFactory.create(kind, data["ID"], data["Name"], float(data["Price"]),
                                 int(data["Stock"]), supplier, extra)

def load_inventory() -> Inventory:
    if not os.path.exists(INVENTORY_FILE):
        return sample_inventory()
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
            records: list[dict] = json.load(file)
        inventory: Inventory = Inventory()
        supplier_cache: dict[str, Supplier] = {}
        for record in records:
            inventory.add_product(product_from_dict(record, supplier_cache))
        return inventory
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Could not load inventory: {error}")
        return sample_inventory()

def save_inventory(inventory: Inventory) -> None:
    records: list[dict] = [product.to_dict() for product in inventory.products]
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)
    # print("Inventory saved.")

def text_input(prompt: str) -> str:
    while True:
        value: str = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")

def number_input(prompt: str, whole: bool = False, minimum: float = 0) -> float | int:
    while True:
        try:
            value = int(input(prompt)) if whole else float(input(prompt))
            if value < minimum:
                print(f"Enter a value of at least {minimum}.")
            else:
                return value
        except ValueError:
            print("Enter a valid number.")

def add_product(inventory: Inventory) -> None:
    kind: str = input("1 = Physical, 2 = Digital: ").strip()
    if kind not in ("1", "2"):
        print("Invalid type.")
        return
    pid: str = text_input("Product ID: ")
    if inventory.find_product(pid) is not None:
        print("Product ID already exists.")
        return
    name: str = text_input("Name: ")
    price: float = get_positive_float("Price: ")
    stock: int = int(number_input("Stock: ", True))
    # Supplier is constructed separately, then associated with the Product.
    supplier: Supplier = Supplier(text_input("Supplier ID: "),
                                  text_input("Supplier name: "),
                                  text_input("Supplier email: "))
    try:
        if kind == "1":
            extra: float = get_positive_float("Weight (kg): ")
            product: Product = ProductFactory.create("physical", pid, name, price, stock, supplier, extra)
        else:
            extra = get_positive_float("Download size (MB): ")
            product = ProductFactory.create("digital", pid, name, price, stock, supplier, extra)
        inventory.add_product(product)
    except ValueError as error:
        print(f"Could not add product: {error}")
        return
    print("Product added.")

def update_stock(inventory: Inventory) -> None:
    product: Product | None = inventory.find_product(text_input("Product ID: "))
    if product is None:
        print("Product not found.")
        return
    try:
        product.update_stock(int(number_input("New stock: ", True)))
        print("Stock updated.")
    except ValueError as error:
        print(f"Could not update stock: {error}")

def search_product(inventory: Inventory) -> None:
    product: Product | None = inventory.find_product(text_input("Product ID: "))
    if product is None:
        print("Product not found.")
    else:
        product.display_information()
        print(product.get_fulfilment_info())

def remove_product(inventory: Inventory) -> None:
    removed: Product | None = inventory.remove_product(text_input("Product ID: "))
    print("Product removed from this Inventory." if removed else "Product not found.")
    # The returned Product object still exists; it is not destroyed by removal.

def choose_discount() -> DiscountStrategy:
    print("Discount: 1 = None, 2 = 10% off, 3 = $20 off orders of $200+, 4 = Student 5%")
    options: dict[str, DiscountStrategy] = {
        "1": NoDiscount(), "2": PercentageDiscount(10),
        "3": BulkDiscount(200, 20), "4": StudentDiscount()}
    choice: str = input("Choose discount: ").strip()
    if choice not in options:
        print("Invalid choice, using no discount.")
        return NoDiscount()
    return options[choice]

def load_products_from_csv(inventory: Inventory) -> None:
    path: str = text_input("CSV file path (e.g. products.csv): ")
    # One shared Supplier for the imported rows (the CSV has no supplier columns).
    supplier: Supplier = Supplier("S000", "CSV Import Supplier", "import@example.com")
    load_products(path, inventory, supplier)

def create_order(inventory: Inventory) -> None:
    order: Order = Order(text_input("Order ID: "), choose_discount())
    while True:
        pid: str = input("Product ID to add (or done): ").strip()
        if pid.lower() == "done":
            break
        product: Product | None = inventory.find_product(pid)
        if product is None:
            print("Product not found.")
            continue
        quantity: int = int(number_input("Quantity: ", True, 1))
        if quantity > product.stock:
            print("Quantity exceeds available stock.")
            continue
        # Main passes Product and quantity; Order constructs OrderLine itself.
        try:
            order.add_order_line(product, quantity)
        except ValueError as error:
            print(f"Could not add line: {error}")
    order.display_order()

def show_product_details(product: Product) -> None:
    # Same function works for both subclasses (LSP + polymorphism).
    product.display_information()
    print(product.get_fulfilment_info())

def demonstrate_polymorphism(inventory: Inventory) -> None:
    for product in inventory.products:  # One loop over list[Product].
        show_product_details(product)

def demonstrate_relationships(inventory: Inventory) -> None:
    if not inventory.products:
        print("Add a product first.")
        return
    product: Product = inventory.products[0]
    other_inventory: Inventory = Inventory()
    moved: Product | None = inventory.remove_product(product.product_id)
    if moved is not None:
        other_inventory.add_product(moved)
        print("Same Product transferred:", other_inventory.find_product(moved.product_id) is product)
        returned: Product | None = other_inventory.remove_product(moved.product_id)
        if returned is not None:
            inventory.add_product(returned)

    first_order: Order = Order("ORD001")
    second_order: Order = Order("ORD002")
    first_order.add_order_line(product, 2)
    second_order.add_order_line(product, 1)
    first_order.display_order()
    second_order.display_order()
    first_line = first_order.get_order_lines()[0]
    second_line = second_order.get_order_lines()[0]
    print("Different OrderLine objects:", first_line is not second_line)
    print("Same Product reference:", first_line.product is second_line.product)

def main() -> None:
    inventory: Inventory = load_inventory()
    while True:
        print("\n--------------MENU--------------")
        print(
            "1. Display All Products\n"
            "2. Add Product\n"
            "3. Update Stock\n"
            "4. Search Product\n"
            "5. Save Inventory\n"
            "6. Remove\n"
            "7. Create Order\n"
            "8. Relationship\n"
            "9. Polymorphism\n"
            "10. Load Products from CSV\n"
            "11. Exit"
        )
        print("--------------------------------")
        option: str = input("Choose: ").strip()
        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            try:
                save_inventory(inventory)
                print("\nInventory saved successfully to inventory.json.")
            except OSError as error:
                print(f"Could not save inventory: {error}")
        elif option == "6":
            remove_product(inventory)
        elif option == "7":
            create_order(inventory)
        elif option == "8":
            demonstrate_relationships(inventory)
        elif option == "9":
            demonstrate_polymorphism(inventory)
        elif option == "10":
            load_products_from_csv(inventory)
        elif option == "11":
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
            print("Invalid option.")

if __name__ == "__main__":
    main()
