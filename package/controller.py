from typing import Dict, List
from .drink import Drink
from .card import Card


class Controller:
    """Business logic for cash and inventory management."""

    def __init__(self) -> None:
        # initial cash reserves for each currency unit
        self.cashes: Dict[int, int] = {1000: 10, 500: 10, 100: 10, 50: 10}
        self.drinks: List[Drink] = []
        self.card = Card()
        self.inserted_cash = 0

    def input_cash(self, amounts: Dict[int, int]) -> None:
        """Accumulate inserted cash and update reserves."""
        for currency, count in amounts.items():
            if currency not in self.cashes:
                continue
            self.cashes[currency] += count
            self.inserted_cash += currency * count

    def refund_cash(self) -> Dict[int, int]:
        refunds: Dict[int, int] = {}
        total_change = self.inserted_cash
        for currency in sorted(self.cashes.keys(), reverse=True):
            while self.cashes[currency] > 0 and total_change >= currency:
                self.cashes[currency] -= 1
                refunds[currency] = refunds.get(currency, 0) + 1
                total_change -= currency
        self.inserted_cash = 0
        return refunds

    def add_drinks(self, drink: Drink) -> None:
        self.drinks.append(drink)

    def dispense(self, drink: Drink) -> str:
        if drink.count <= 0:
            return "재고 없음"
        if self.inserted_cash >= drink.price or self.card.status:
            drink.count -= 1
            self.inserted_cash -= drink.price
            return "음료 제공"
        return "잔액 부족"
