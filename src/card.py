class Card:
    """Simple card authorization model."""

    def __init__(self) -> None:
        self.status = False

    def accept(self) -> bool:
        """Process card payment and return approval status."""
        self.status = True
        return self.status
