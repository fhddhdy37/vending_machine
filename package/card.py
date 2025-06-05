import re


class Card:
    """Simple card authorization model for handling card transactions."""

    # Predefined valid card numbers
    __CARD_ID = [
        "ABCDE12345",
        "12345ABCDE",
        "A1B2C3D4E5",
    ]

    def __init__(self) -> None:
        # True when payment is approved
        self.status = False
        # True when a card has been inserted
        self.inserted = False
        # Store the inserted card number
        self.number: str = ""

    def insert_card(self, number: str) -> bool:
        """Validate the card and register it if valid."""
        pattern = r"^[A-Za-z0-9]{10}$"
        if re.fullmatch(pattern, number) and number in self.__CARD_ID:
            self.number = number
            self.inserted = True
            self.status = False
            return True
        return False

    def approve(self) -> None:
        """Approve the pending card transaction."""
        self.status = True

    def reset(self) -> None:
        """Reset card information after a transaction is completed."""
        self.number = ""
        self.inserted = False
        self.status = False

    def accept(self) -> bool:
        """Backward compatibility method returning approval status."""
        self.approve()
        return self.status
