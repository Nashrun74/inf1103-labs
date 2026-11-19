from product import Product

class Inventory:
    def __init__(self) -> None:
        # One collection for the abstract Product type supports both subclasses.
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if self.find_product(product.product_id) is not None:
            raise ValueError("Product ID already exists.")
        self.products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        product: Product | None = self.find_product(product_id)
        if product is not None:
            self.products.remove(product)
        # Return the same object: it can be used or transferred elsewhere.
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def display_all(self) -> None:
        if not self.products:
            print("Inventory is empty.")
            return
        # Polymorphism: no subclass checks or separate loops.
        for product in self.products:
            product.display_information()
            print(product.get_fulfilment_info())
