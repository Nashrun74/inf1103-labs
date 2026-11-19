from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

class ProductFactory:
    """Single place that knows which concrete Product class to build.
    Returns the abstract Product type, so callers stay decoupled."""

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra: float = 1.0) -> Product:
        # extra = weight (kg) for physical products, download size (MB) for digital.
        kind: str = product_type.strip().lower()
        if kind == "physical":
            return PhysicalProduct(product_id, name, price, stock, extra, supplier)
        elif kind == "digital":
            return DigitalProduct(product_id, name, price, stock, extra, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
