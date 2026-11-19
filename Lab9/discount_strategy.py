from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """Common interface for every discount. Order only ever calls apply()."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass
