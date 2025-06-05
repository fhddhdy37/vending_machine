from dataclasses import dataclass


@dataclass
class Drink:
    """자판기에 들어가는 음료 정보를 표현한다."""

    name: str
    price: int
    count: int
    image_path: str

