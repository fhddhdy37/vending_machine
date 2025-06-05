from typing import Dict, List
from .drink import Drink
from .card import Card


class Controller:
    """현금과 재고 관리를 처리하는 비즈니스 로직 클래스."""

    def __init__(self) -> None:
        """초기 현금 시재와 카드 모듈을 설정한다."""
        # 화폐 단위별 초기 시재
        self.cashes: Dict[int, int] = {1000: 10, 500: 10, 100: 10, 50: 10}
        self.drinks: List[Drink] = []
        self.card = Card()
        self.inserted_cash = 0

    def input_cash(self, amounts: Dict[int, int]) -> None:
        """투입된 현금을 누적하여 시재에 반영한다."""
        for currency, count in amounts.items():
            if currency not in self.cashes:
                continue
            self.cashes[currency] += count
            self.inserted_cash += currency * count

    def refund_cash(self) -> Dict[int, int]:
        """투입된 금액을 화폐 단위별로 반환한다."""
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
        """음료 객체를 재고 목록에 추가한다."""
        self.drinks.append(drink)

    def dispense(self, drink: Drink) -> str:
        """음료 재고와 결제 상태를 확인하여 상품을 제공한다."""
        if drink.count <= 0:
            return "재고 없음"
        if self.inserted_cash >= drink.price:
            drink.count -= 1
            self.inserted_cash -= drink.price
            return "음료 제공"
        if self.card.status:
            drink.count -= 1
            return "음료 제공"
        return "잔액 부족"
