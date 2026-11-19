from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size <= 0:
            raise ValueError("Download size must be greater than zero.")
        self.__download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print("Product Type: Digital")
        print(f"Download Size: {self.__download_size:.2f} MB")
        print(f"Fulfilment: {self.get_fulfilment_info()}")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def to_dict(self) -> dict:
        return {"type": "digital", "ID": self.product_id, "Name": self.name,
                "Price": self.price, "Stock": self.stock,
                "DownloadSize": self.__download_size,
                "Supplier": {"SupplierID": self.supplier.supplier_id,
                             "Name": self.supplier.name,
                             "ContactEmail": self.supplier.contact_email}}
