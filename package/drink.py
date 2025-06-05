from dataclasses import dataclass


@dataclass
class Drink:
    """자판기에 들어가는 음료 정보를 표현한다.

    Attributes
    ----------
    name : str
        음료 이름.
    price : int
        판매 가격.
    count : int
        현재 재고 수량.
    image_path : str
        버튼에 표시할 이미지 파일 경로.
    """

    name: str
    price: int
    count: int
    image_path: str

