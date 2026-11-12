from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 weight: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print("Product Type: Physical")
        print(f"Weight: {self.__weight:.2f} kg")
        print(f"Fulfilment: {self.get_fulfilment_info()}")
        print(f"Shipping Cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        # Example lab formula: $2.00 base + $1.50 per kg.
        return 2.00 + self.__weight * 1.50

    def to_dict(self) -> dict:
        return {"type": "physical", "ID": self.product_id, "Name": self.name,
                "Price": self.price, "Stock": self.stock, "Weight": self.__weight,
                "Supplier": {"SupplierID": self.supplier.supplier_id,
                             "Name": self.supplier.name,
                             "ContactEmail": self.supplier.contact_email}}
