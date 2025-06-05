import re


class Card:
    """카드 결제를 위한 간단한 인증 모델."""

    # Predefined valid card numbers
    __CARD_ID = [
        "ABCDE12345",
        "12345ABCDE",
        "A1B2C3D4E5",
    ]

    def __init__(self) -> None:
        """카드 상태와 번호를 초기화한다."""
        # 결제 승인 여부
        self.status = False
        # 카드 삽입 여부
        self.inserted = False
        # 삽입된 카드 번호
        self.number: str = ""

    def insert_card(self, number: str) -> bool:
        """카드 번호를 검증하고 유효하면 등록한다."""
        pattern = r"^[A-Za-z0-9]{10}$"
        if re.fullmatch(pattern, number) and number in self.__CARD_ID:
            self.number = number
            self.inserted = True
            self.status = False
            return True
        return False

    def approve(self) -> None:
        """대기 중인 카드 결제를 승인한다."""
        self.status = True

    def reset(self) -> None:
        """거래 완료 후 카드 정보를 초기화한다."""
        self.number = ""
        self.inserted = False
        self.status = False

    def accept(self) -> bool:
        """호환성을 위해 승인 상태를 반환한다."""
        self.approve()
        return self.status
