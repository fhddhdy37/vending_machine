import tkinter as tk

from package.machine import Machine
from package.drink import Drink

def main() -> None:
    """자판기 프로그램의 진입점.

    ``tk.Tk`` 루트 윈도우를 생성하고 :class:`Machine` 객체를 초기화한 뒤,
    ``drink_infos`` 목록을 활용하여 기본 음료 재고를 채운다.
    """
    root = tk.Tk()
    machine = Machine(root)
    
    # Define the vending machine drinks. The first two are water priced at 800
    # won. All other drinks cost between 1000 and 1800 won. Each image may be
    # reused, but no drink type appears more than twice in a row and a variety
    # of names is used.
    drink_infos = [
        ("물", 800, "src/drinks/water.png"),
        ("물", 800, "src/drinks/water.png"),
        ("레몬에이드", 1000, "src/drinks/ade.png"),
        ("자몽에이드", 1000, "src/drinks/ade.png"),
        ("칠성 사이다", 1100, "src/drinks/cider.png"),
        ("제로 사이다", 1100, "src/drinks/cider.png"),
        ("코카콜라", 1200, "src/drinks/coke.png"),
        ("코카콜라 제로", 1200, "src/drinks/coke.png"),
        ("환타 오렌지", 1300, "src/drinks/fanta.png"),
        ("환타 파인애플", 1300, "src/drinks/fanta.png"),
        ("이온워터", 1400, "src/drinks/ion.png"),
        ("파워 이온", 1400, "src/drinks/ion.png"),
        ("청량 탄산수", 1500, "src/drinks/soda.png"),
        ("라임 탄산수", 1500, "src/drinks/soda.png"),
        ("아이스 블루", 1600, "src/drinks/ade.png"),
        ("자몽 스파클", 1600, "src/drinks/ade.png"),
        ("더블 사이다", 1700, "src/drinks/cider.png"),
        ("스위트 사이다", 1700, "src/drinks/cider.png"),
        ("고급 콜라", 1800, "src/drinks/coke.png"),
        ("다크 콜라", 1800, "src/drinks/coke.png"),
        ("환타 포도", 1100, "src/drinks/fanta.png"),
        ("환타 레몬", 1100, "src/drinks/fanta.png"),
        ("하이드레이션 워터", 1200, "src/drinks/ion.png"),
        ("스포츠 워터", 1200, "src/drinks/ion.png"),
    ]

    # Fill the vending machine with drinks. Images will be displayed on buttons.
    for i in range(24):
        name, price, image = drink_infos[i % len(drink_infos)]
        machine.controller.add_drinks(Drink(name, price, 10, image))
        
    machine.refresh_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
