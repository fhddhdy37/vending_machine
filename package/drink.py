from dataclasses import dataclass


@dataclass
class Drink:
    """Represents a drink item in the vending machine."""

    name: str
    price: int
    count: int
    image_path: str

