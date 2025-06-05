import re


class Card:
    """카드 결제를 위한 간단한 인증 모델.

    주요 속성으로 ``status``(결제 승인 여부), ``inserted``(카드 삽입 상태),
    ``number``(삽입된 카드 번호)을 관리한다.
    """

    # Predefined valid card numbers
    __CARD_ID = [
        "ABCDE12345",
        "12345ABCDE",
        "A1B2C3D4E5",
    ]

    def __init__(self) -> None:
        """카드 상태와 번호를 초기화한다.

        매개변수는 없으며 ``status``와 ``inserted``를 ``False``로,
        ``number``를 빈 문자열로 설정하여 초기 상태를 만든다.
        """
        # 결제 승인 여부
        self.status = False
        # 카드 삽입 여부
        self.inserted = False
        # 삽입된 카드 번호
        self.number: str = ""

    def insert_card(self, number: str) -> bool:
        """카드 번호를 검증하고 유효하면 등록한다.

        Parameters
        ----------
        number : str
            10자리 영문/숫자로 이루어진 카드 번호.

        ``__CARD_ID`` 목록과 비교하여 일치하면 ``number``와 ``inserted``를
        갱신하고 ``status``를 초기화한다.
        """
        pattern = r"^[A-Za-z0-9]{10}$"
        if re.fullmatch(pattern, number) and number in self.__CARD_ID:
            self.number = number
            self.inserted = True
            self.status = False
            return True
        return False

    def approve(self) -> None:
        """대기 중인 카드 결제를 승인한다.

        ``status`` 값을 ``True``로 변경하여 승인 완료 상태로 만든다.
        """
        self.status = True

    def reset(self) -> None:
        """거래 완료 후 카드 정보를 초기화한다.

        ``number``를 비우고 ``inserted``와 ``status``를 ``False``로 되돌린다.
        """
        self.number = ""
        self.inserted = False
        self.status = False

    def accept(self) -> bool:
        """호환성을 위해 승인 상태를 반환한다.

        내부적으로 :py:meth:`approve` 를 호출하여 ``status`` 값을 갱신하고
        그 값을 그대로 반환한다.
        """
        self.approve()
        return self.status
