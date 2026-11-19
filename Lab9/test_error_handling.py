import contextlib
import io
import os
import tempfile
import unittest
from unittest.mock import patch

from supplier import Supplier
from inventory import Inventory
from input_helpers import get_positive_float
from product_loader import load_products

CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_quiet(func, *args):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestGetPositiveFloat(unittest.TestCase):
    def test_valid_first_try(self):
        with patch("builtins.input", side_effect=["12.50"]):
            value, _ = run_quiet(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)

    def test_reprompts_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "0", "nan", "12.50"]) as mocked:
            value, out = run_quiet(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(mocked.call_count, 5)
        self.assertIn("Please enter a valid number", out)
        self.assertIn("greater than zero", out)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S0", "Import", "i@test.example")
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "products.csv")
        with open(self.path, "w", newline="", encoding="utf-8") as f:
            f.write(CSV_TEXT)

    def tearDown(self):
        self.tmp.cleanup()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        inv = Inventory()
        _, out = run_quiet(load_products, self.path, inv, self.supplier)
        self.assertEqual([p.product_id for p in inv.products], ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", out)
        self.assertIn("Skipping line 5", out)
        self.assertIn("3 products loaded.", out)
        self.assertTrue(out.strip().endswith("Load attempt finished."))

    def test_missing_file_handled(self):
        inv = Inventory()
        _, out = run_quiet(load_products, os.path.join(self.tmp.name, "nope.csv"), inv, self.supplier)
        self.assertEqual(inv.products, [])
        self.assertIn("Products file not found", out)
        self.assertNotIn("products loaded", out)
        self.assertIn("Load attempt finished.", out)

    def test_duplicate_id_row_reported_and_skipped(self):
        inv = Inventory()
        run_quiet(load_products, self.path, inv, self.supplier)
        _, out = run_quiet(load_products, self.path, inv, self.supplier)
        self.assertIn("Product ID already exists.", out)
        self.assertEqual(len(inv.products), 3)


if __name__ == "__main__":
    unittest.main()
