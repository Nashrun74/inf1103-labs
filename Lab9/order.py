from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy
from no_discount import NoDiscount

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        # Private collection: manage lines through Order methods.
        self.__order_lines: list[OrderLine] = []
        # Association: the strategy is created elsewhere and only used here.
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition: Order creates the OrderLine internally.
        line: OrderLine = OrderLine(product, quantity)
        self.__order_lines.append(line)

    def remove_order_line(self, line_number: int) -> bool:
        if line_number < 1 or line_number > len(self.__order_lines):
            return False
        self.__order_lines.pop(line_number - 1)
        return True

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        # No branching on discount type: the strategy decides how to discount.
        return self.__discount.apply(self.calculate_subtotal())

    def display_order(self) -> None:
        print(f"\nOrder: {self.order_id}")
        for line in self.__order_lines:
            line.display_information()
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Order Total: ${self.calculate_total():.2f}")

    def get_order_lines(self) -> list[OrderLine]:
        # A copy prevents external code from modifying the owned list.
        return self.__order_lines.copy()
