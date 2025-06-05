import tkinter as tk

from package.machine import Machine
from package.drink import Drink

def main() -> None:
    root = tk.Tk()
    machine = Machine(root)

    # Define available drinks with associated images
    drink_infos = [
        ("사이다", 600, "src/drinks/cider.png"),
        ("콜라", 700, "src/drinks/coke.png"),
        ("환타", 700, "src/drinks/fanta.png"),
        ("이온음료", 800, "src/drinks/ion.png"),
        ("에이드", 800, "src/drinks/ade.png"),
        ("소다", 650, "src/drinks/soda.png"),
        ("생수", 500, "src/drinks/water.png"),
    ]

    # Fill the vending machine with drinks. Images will be displayed on buttons.
    for i in range(24):
        name, price, image = drink_infos[i % len(drink_infos)]
        count = 0 if i % 2 == 0 else 5
        machine.controller.add_drinks(Drink(name, price, count, image))
        
    machine.refresh_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
