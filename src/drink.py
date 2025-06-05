class Drink:
    """Represents a drink item in the vending machine."""

    def __init__(self, name: str, price: int, count: int) -> None:
        self.name = name
        self.price = price
        self.count = count
