from discount_strategy import DiscountStrategy

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        # Takes the amount off any total at or above the threshold.
        if total >= self.__threshold:
            return total - self.__amount
        return total
