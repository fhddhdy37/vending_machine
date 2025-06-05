class Card:
    """Simple card authorization model for handling card transactions."""

    def __init__(self) -> None:
        # True when payment is approved
        self.status = False
        # True when a card has been inserted
        self.inserted = False
        # Store the inserted card number
        self.number: str = ""

    def insert_card(self, number: str) -> None:
        """Register a card number and mark it as inserted."""
        self.number = number
        self.inserted = True
        self.status = False

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
