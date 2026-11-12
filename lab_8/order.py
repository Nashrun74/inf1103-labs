from product import Product
from order_line import OrderLine

class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        # Private collection: manage lines through Order methods.
        self.__order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition: Order creates the OrderLine internally.
        line: OrderLine = OrderLine(product, quantity)
        self.__order_lines.append(line)

    def remove_order_line(self, line_number: int) -> bool:
        if line_number < 1 or line_number > len(self.__order_lines):
            return False
        self.__order_lines.pop(line_number - 1)
        return True

    def calculate_total(self) -> float:
        total: float = 0.0
        for line in self.__order_lines:
            total += line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print(f"\nOrder: {self.order_id}")
        for line in self.__order_lines:
            line.display_information()
        print(f"Order Total: ${self.calculate_total():.2f}")

    def get_order_lines(self) -> list[OrderLine]:
        # A copy prevents external code from modifying the owned list.
        return self.__order_lines.copy()
