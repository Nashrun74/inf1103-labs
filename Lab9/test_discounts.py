import inspect
import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount
from percentage_discount import PercentageDiscount
from bulk_discount import BulkDiscount
from student_discount import StudentDiscount


def make_order(discount=None) -> Order:
    supplier = Supplier("S1", "Test Supplier", "s@test.example")
    product = ProductFactory.create("physical", "P1", "Item", 50.0, 10, supplier, 1.0)
    order = Order("O1", discount)
    order.add_order_line(product, 5)  # 5 x 50 = 250
    return order


class TestDiscountStrategies(unittest.TestCase):
    def test_default_is_no_discount(self):
        self.assertEqual(make_order().calculate_total(), 250.0)

    def test_no_discount(self):
        self.assertEqual(NoDiscount().apply(100), 100)

    def test_percentage(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225.0)

    def test_percentage_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(120)

    def test_bulk_at_and_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)

    def test_bulk_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_student(self):
        self.assertAlmostEqual(StudentDiscount().apply(100), 95.0)

    def test_all_are_discount_strategies(self):
        for s in (NoDiscount(), PercentageDiscount(5), BulkDiscount(1, 1), StudentDiscount()):
            self.assertIsInstance(s, DiscountStrategy)


class TestOrderUsesStrategy(unittest.TestCase):
    def test_order_total_through_strategy(self):
        self.assertEqual(make_order(BulkDiscount(200, 20)).calculate_total(), 230)

    def test_set_discount_changes_strategy(self):
        order = make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_needs_no_change_to_order(self):
        # A brand-new strategy defined here works with the unchanged Order class.
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2
        self.assertEqual(make_order(HalfPrice()).calculate_total(), 125.0)

    def test_order_has_no_discount_branching(self):
        source = inspect.getsource(Order)
        self.assertNotIn("elif", source)
        for word in ("percentage", "bulk", "student"):
            self.assertNotIn(word, source.lower())

    def test_two_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        a, b = make_order(shared), make_order(shared)
        self.assertAlmostEqual(a.calculate_total(), b.calculate_total())


if __name__ == "__main__":
    unittest.main()
