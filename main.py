import tkinter as tk

from package.machine import Machine
from package.drink import Drink


def main() -> None:
    root = tk.Tk()
    machine = Machine(root)

    for i in range(24):
        image = "src/drinks/water.png"
        machine.controller.add_drinks(
            Drink("물", 500, 0 if i % 2 == 0 else 5, image)
        )

    machine.refresh_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
