import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from .controller import Controller
from .drink import Drink


class Machine:
    """GUI logic for the vending machine."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.controller = Controller()
        self.root.title("자판기 시스템")
        # adjust window size as requested
        self.root.geometry("1000x500")
        self.images: list[ImageTk.PhotoImage] = []
        self.build_frame()

    def build_frame(self) -> None:
        drink_frame = tk.Frame(self.root, bg="black")
        drink_frame.grid(row=0, column=0, padx=5, pady=5)

        for i in range(4):
            for j in range(6):
                index = i * 6 + j
                if index < len(self.controller.drinks):
                    drink = self.controller.drinks[index]
                    state = "X 구매 불가" if drink.count <= 0 else f"{drink.price}원"
                    fg_color = "red" if drink.count <= 0 else "white"
                    img = self.load_image(drink.image_path)
                    btn = tk.Button(
                        drink_frame,
                        text=f"{drink.name}\n{state}",
                        image=img,
                        compound="top",
                        fg=fg_color,
                        bg="black",
                        width=12,
                        height=8,
                        command=lambda d=drink: self.select_drink(d),
                        relief="groove",
                    )
                    self.images.append(img)
                    btn.grid(row=i, column=j, padx=5, pady=5)

        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=1, sticky="n")

        blue_panel = tk.Frame(right_frame, width=300, height=200, bg="blue")
        blue_panel.pack_propagate(False)
        blue_panel.pack(pady=5)

        orange_panel = tk.Frame(right_frame, bg="orange", width=300, height=50)
        orange_panel.pack_propagate(False)
        orange_panel.pack()
        self.cash_label = tk.Label(
            orange_panel,
            text=f"투입된 금액 : {self.controller.inserted_cash}원",
            bg="orange",
            font=("맑은 고딕", 12),
        )
        self.cash_label.pack()

        control_panel = tk.Frame(right_frame)
        control_panel.pack(pady=10)

        self.cash_var = tk.IntVar(value=1000)
        tk.OptionMenu(control_panel, self.cash_var, 1000, 500, 100, 50).grid(row=0, column=0)
        tk.Button(control_panel, text="투입", command=self.insert_cash).grid(row=0, column=1, padx=5)
        tk.Button(control_panel, text="반환", command=self.refund).grid(row=0, column=2, padx=5)

        self.card_status = tk.Label(
            right_frame, text="카드 상태: 대기 중", bg="white", width=35
        )
        self.card_status.pack(pady=5)

        tk.Button(right_frame, text="카드 투입", bg="green", fg="white", command=self.use_card).pack()

        admin_btn = tk.Button(right_frame, text="🔑", command=self.admin_menu, bg="white")
        admin_btn.place(relx=0.95, rely=0.95, anchor="se")

    def refresh_gui(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_frame()

    def insert_cash(self) -> None:
        amount = self.cash_var.get()
        self.controller.input_cash({amount: 1})
        self.refresh_gui()

    def refund(self) -> None:
        change = self.controller.refund_cash()
        msg = "\n".join([f"{k}원: {v}개" for k, v in change.items()])
        messagebox.showinfo("거스름돈 반환", msg or "반환할 금액이 없습니다.")
        self.refresh_gui()

    def use_card(self) -> None:
        if self.controller.card.accept():
            self.card_status.config(text="카드 상태: 승인 완료")
            messagebox.showinfo("카드 결제", "결제가 승인되었습니다.")
        else:
            self.card_status.config(text="카드 상태: 결제 실패")
        self.refresh_gui()

    def select_drink(self, drink: Drink) -> None:
        result = self.controller.dispense(drink)
        messagebox.showinfo("음료 선택", result)
        self.refresh_gui()

    def admin_menu(self) -> None:
        messagebox.showinfo("관리자 모드", "관리자 메뉴로 진입합니다. (구현 예정)")

    def load_image(self, path: str) -> ImageTk.PhotoImage:
        """Load and resize the given image path safely."""
        if not os.path.exists(path):
            img = Image.new("RGB", (70, 70), color="gray")
        else:
            img = Image.open(path)
        img = img.resize((70, 70))
        return ImageTk.PhotoImage(img)
