from discount_strategy import DiscountStrategy

class StudentDiscount(DiscountStrategy):
    """Fourth strategy: a fixed 5% student discount.
    Added as a new class only - Order was not modified (OCP)."""
    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)
