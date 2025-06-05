from typing import Dict, List
from .drink import Drink
from .card import Card


class Controller:
    """현금과 재고 관리를 처리하는 비즈니스 로직 클래스.

    ``cashes``(화폐 단위별 시재), ``drinks``(음료 리스트), ``card``(카드 모듈)
    그리고 ``inserted_cash``(투입된 총 금액)을 속성으로 보유한다.
    """

    def __init__(self) -> None:
        """초기 현금 시재와 카드 모듈을 설정한다.

        ``cashes`` 딕셔너리에 기본 시재를 채우고 ``card`` 인스턴스를 생성하며
        ``inserted_cash`` 값을 0으로 초기화한다.
        """
        # 화폐 단위별 초기 시재
        self.cashes: Dict[int, int] = {1000: 10, 500: 10, 100: 10, 50: 10}
        self.drinks: List[Drink] = []
        self.card = Card()
        self.inserted_cash = 0

    def input_cash(self, amounts: Dict[int, int]) -> None:
        """투입된 현금을 누적하여 시재에 반영한다.

        Parameters
        ----------
        amounts : Dict[int, int]
            ``{화폐단위: 개수}`` 형태로 전달되는 투입 금액 정보.

        각 화폐 단위를 ``cashes``에 더하고 ``inserted_cash`` 총액을 갱신한다.
        """
        for currency, count in amounts.items():
            if currency not in self.cashes:
                continue
            self.cashes[currency] += count
            self.inserted_cash += currency * count

    def refund_cash(self) -> Dict[int, int]:
        """투입된 금액을 화폐 단위별로 반환한다.

        ``cashes``에서 거스름돈을 차감하며 ``inserted_cash``를 0으로 초기화한다.
        반환 값은 거슬러 준 화폐 단위별 개수를 담은 딕셔너리이다.
        """
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
        """음료 객체를 재고 목록에 추가한다.

        Parameters
        ----------
        drink : :class:`Drink`
            재고 목록에 등록할 음료 객체.

        ``drinks`` 리스트에 전달된 음료를 추가한다.
        """
        self.drinks.append(drink)

    def dispense(self, drink: Drink) -> str:
        """음료 재고와 결제 상태를 확인하여 상품을 제공한다.

        Parameters
        ----------
        drink : :class:`Drink`
            선택된 음료 객체.

        ``inserted_cash``나 ``card.status``가 충분하면 재고를 차감하고 결과
        문자열을 반환한다.
        """
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
