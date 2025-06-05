import tkinter as tk

from src.machine import Machine
from src.drink import Drink


def main() -> None:
    root = tk.Tk()
    machine = Machine(root)

    for i in range(24):
        machine.controller.add_drinks(Drink("물", 500, 0 if i % 2 == 0 else 5))

    machine.refresh_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
