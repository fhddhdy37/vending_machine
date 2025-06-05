import tkinter as tk
from tkinter import messagebox

class Drink:
    def __init__(self, name, price, count):
        self.name = name
        self.price = price
        self.count = count

class Card:
    def __init__(self):
        self.status = False

    def accept(self):
        self.status = True
        return self.status

class Controller:
    def __init__(self):
        self.cashes = {1000: 10, 500: 10, 100: 10, 50: 10}
        self.drinks = []
        self.card = Card()
        self.inserted_cash = 0

    def input_cash(self, amount):
        self.inserted_cash += amount
        self.cashes[amount] += 1

    def refund_cash(self):
        refunds = {}
        total_change = self.inserted_cash
        for currency in sorted(self.cashes.keys(), reverse=True):
            while self.cashes[currency] > 0 and total_change >= currency:
                self.cashes[currency] -= 1
                refunds[currency] = refunds.get(currency, 0) + 1
                total_change -= currency
        self.inserted_cash = 0
        return refunds

    def add_drinks(self, drink):
        self.drinks.append(drink)

    def dispense(self, drink):
        if drink.count <= 0:
            return "재고 없음"
        if self.inserted_cash >= drink.price or self.card.status:
            drink.count -= 1
            self.inserted_cash -= drink.price
            return "음료 제공"
        else:
            return "잔액 부족"

class Machine:
    def __init__(self, root):
        self.root = root
        self.controller = Controller()
        self.root.title("자판기 시스템")
        self.root.geometry("1100x700")
        self.build_frame()

    def build_frame(self):
        # 좌측 음료 프레임
        drink_frame = tk.Frame(self.root, bg="black")
        drink_frame.grid(row=0, column=0, padx=10, pady=10)

        for i in range(4):
            for j in range(6):
                index = i * 6 + j
                if index < len(self.controller.drinks):
                    drink = self.controller.drinks[index]
                    state = "X 구매 불가" if drink.count <= 0 else f"{drink.price}원"
                    fg_color = "red" if drink.count <= 0 else "white"
                    btn = tk.Button(
                        drink_frame,
                        text=f"{drink.name}\n{state}",
                        fg=fg_color,
                        bg="black",
                        width=14,
                        height=6,
                        command=lambda d=drink: self.select_drink(d),
                        relief="groove"
                    )
                    btn.grid(row=i, column=j, padx=5, pady=5)

        # 우측 전체 프레임
        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=1, sticky="n")

        # 상단 파란 배경 영역
        blue_panel = tk.Frame(right_frame, width=400, height=300, bg="blue")
        blue_panel.pack_propagate(False)
        blue_panel.pack(pady=5)

        # 하단 주황색 패널
        orange_panel = tk.Frame(right_frame, bg="orange", width=400, height=50)
        orange_panel.pack_propagate(False)
        orange_panel.pack()
        self.cash_label = tk.Label(orange_panel, text=f"투입된 금액 : {self.controller.inserted_cash}원", bg="orange", font=("맑은 고딕", 12))
        self.cash_label.pack()

        # 금액 선택 및 버튼
        control_panel = tk.Frame(right_frame)
        control_panel.pack(pady=10)

        self.cash_var = tk.IntVar(value=1000)
        tk.OptionMenu(control_panel, self.cash_var, 1000, 500, 100, 50).grid(row=0, column=0)
        tk.Button(control_panel, text="투입", command=self.insert_cash).grid(row=0, column=1, padx=5)
        tk.Button(control_panel, text="반환", command=self.refund).grid(row=0, column=2, padx=5)

        # 카드 결제 상태
        self.card_status = tk.Label(right_frame, text="카드 상태: 대기 중", bg="white", width=40)
        self.card_status.pack(pady=5)

        tk.Button(right_frame, text="카드 투입", bg="green", fg="white", command=self.use_card).pack()

        # 관리자 버튼 (열쇠 아이콘 대신 '🔑' 텍스트 사용)
        admin_btn = tk.Button(right_frame, text="🔑", command=self.admin_menu, bg="white")
        admin_btn.place(relx=0.95, rely=0.95, anchor="se")

    def refresh_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_frame()

    def insert_cash(self):
        amount = self.cash_var.get()
        self.controller.input_cash(amount)
        self.refresh_gui()

    def refund(self):
        change = self.controller.refund_cash()
        msg = "\n".join([f"{k}원: {v}개" for k, v in change.items()])
        messagebox.showinfo("거스름돈 반환", msg or "반환할 금액이 없습니다.")
        self.refresh_gui()

    def use_card(self):
        if self.controller.card.accept():
            self.card_status.config(text="카드 상태: 승인 완료")
            messagebox.showinfo("카드 결제", "결제가 승인되었습니다.")
        else:
            self.card_status.config(text="카드 상태: 결제 실패")
        self.refresh_gui()

    def select_drink(self, drink):
        result = self.controller.dispense(drink)
        messagebox.showinfo("음료 선택", result)
        self.refresh_gui()

    def admin_menu(self):
        messagebox.showinfo("관리자 모드", "관리자 메뉴로 진입합니다. (구현 예정)")


if __name__ == "__main__":
    root = tk.Tk()
    machine = Machine(root)

    # 예시 음료 24개 채우기
    for i in range(24):
        machine.controller.add_drinks(Drink("물", 500, 0 if i % 2 == 0 else 5))

    machine.refresh_gui()
    root.mainloop()
