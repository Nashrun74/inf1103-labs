import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
from order_line import OrderLine

SUPPLIER = Supplier("S1", "Test Supplier", "s@test.example")


class TestProductFactory(unittest.TestCase):
    def test_creates_physical(self):
        p = ProductFactory.create("physical", "P1", "Lamp", 25.0, 10, SUPPLIER, 1.2)
        self.assertIsInstance(p, PhysicalProduct)
        self.assertIsInstance(p, Product)

    def test_creates_digital(self):
        p = ProductFactory.create("digital", "D1", "App", 49.9, 100, SUPPLIER, 20.0)
        self.assertIsInstance(p, DigitalProduct)

    def test_type_is_case_insensitive(self):
        self.assertIsInstance(ProductFactory.create("PHYSICAL", "P1", "x", 1, 1, SUPPLIER), PhysicalProduct)

    def test_unknown_type_raises_clear_message(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "Install", 30.0, 5, SUPPLIER)
        self.assertEqual(str(ctx.exception), "Unknown product type: service")


class TestValidation(unittest.TestCase):
    def test_price_must_be_positive(self):
        for bad in (0, -1):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P1", "x", bad, 1, SUPPLIER)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "x", 5.0, -1, SUPPLIER)

    def test_zero_stock_allowed(self):
        self.assertEqual(ProductFactory.create("digital", "D1", "x", 5.0, 0, SUPPLIER).stock, 0)

    def test_update_stock_negative_rejected_for_both_subclasses(self):
        # LSP: both subclasses keep the rule defined by Product.
        for kind in ("physical", "digital"):
            p = ProductFactory.create(kind, "X1", "x", 5.0, 3, SUPPLIER)
            with self.assertRaises(ValueError):
                p.update_stock(-5)
            self.assertEqual(p.stock, 3)

    def test_order_line_quantity_must_be_positive(self):
        p = ProductFactory.create("physical", "P1", "x", 5.0, 3, SUPPLIER)
        for bad in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(p, bad)


if __name__ == "__main__":
    unittest.main()
