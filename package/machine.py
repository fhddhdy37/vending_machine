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
        self.root.geometry("948x431")
        self.root.configure(bg="black")
        self.images: list[ImageTk.PhotoImage] = []
        self.build_frame()

    def build_frame(self) -> None:
        drink_frame = tk.Frame(self.root, bg="black")
        drink_frame.grid(row=0, column=0)

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
                        width=100,
                        height=100,
                        command=lambda d=drink: self.select_drink(d),
                        relief="groove",
                    )
                    self.images.append(img)
                    btn.grid(row=i, column=j)

        right_frame = tk.Frame(self.root, bg="black")
        right_frame.grid(row=0, column=1, sticky="ns")

        admin_panel = tk.Frame(right_frame, width=300, height=200, bg="black")
        admin_panel.pack_propagate(False)
        admin_panel.pack()

        cash_panel = tk.Frame(right_frame, bg="black", width=300, height=50)
        cash_panel.pack_propagate(False)
        cash_panel.pack()

        # cash_panel 내부를 2개의 열로 나누기
        cash_panel.grid_columnconfigure(0, weight=1)  # 첫 번째 열
        cash_panel.grid_columnconfigure(1, weight=1)  # 두 번째 열

        # "투입된 금액" 텍스트를 위한 프레임
        cash_text_frame = tk.Frame(cash_panel, bg="black")
        cash_text_frame.grid(row=0, column=0, sticky="ew", padx=5)

        cash_text_label = tk.Label(
            cash_text_frame,
            text="투입된 금액 :",
            bg="black",
            fg="white",
            font=("맑은 고딕", 14, "bold"),
        )
        cash_text_label.pack_propagate(False)
        cash_text_label.pack()

        # 실제 금액을 위한 프레임
        cash_value_frame = tk.Frame(cash_panel, bg="black")
        cash_value_frame.grid(row=0, column=1, sticky="ew", padx=5)

        self.cash_label = tk.Label(
            cash_value_frame,
            text=f"{self.controller.inserted_cash}원",
            bg="black",
            fg="white",
            font=("맑은 고딕", 14, "bold"),
        )
        self.cash_label.pack()

        control_panel = tk.Frame(right_frame, bg="black")
        control_panel.pack()

        self.cash_var = tk.IntVar(value=1000)
        tk.OptionMenu(control_panel, self.cash_var, 1000, 500, 100, 50).grid(row=0, column=0)
        tk.Button(control_panel, text="투입", bg="green", fg="white", command=self.insert_cash).grid(row=0, column=1, padx=5)
        tk.Button(control_panel, text="반환", bg="red", fg="white", command=self.refund).grid(row=0, column=2, padx=5)

        card_frame = tk.Frame(right_frame, bg="black")
        card_frame.pack(side="bottom", pady=5)

        self.card_status = tk.Label(
            card_frame,
            text="카드 상태: 대기 중",
            bg="darkgreen",
            font=("맑은 고딕", 10, "bold"),
            width=35,
            height=3,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=1,
        )
        self.card_status.pack(side="top", pady=5)

        entry_button_frame = tk.Frame(card_frame, bg="black")
        entry_button_frame.pack(side="bottom", pady=5)

        self.card_entry = tk.Entry(entry_button_frame, width=20)
        self.card_entry.pack(side="left", padx=5)

        tk.Button(
            entry_button_frame,
            text="카드 투입",
            bg="green",
            fg="white",
            command=self.use_card,
        ).pack(side="left", padx=5)

        # Use a keyhole image for the admin button and place it at the
        # bottom-right corner of the admin panel
        admin_img = self.load_image("src/drinks/keyhole.png", (15, 15))
        admin_btn = tk.Button(admin_panel, image=admin_img, command=self.admin_menu, bg="white")
        self.images.append(admin_img)
        admin_btn.place(relx=1.0, rely=1.0, anchor="se")

    def refresh_gui(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_frame()

    def insert_cash(self) -> None:
        amount = self.cash_var.get()
        self.controller.input_cash({amount: 1})
        # Update only the cash label instead of rebuilding the entire GUI
        self.cash_label.config(
            text=f"{self.controller.inserted_cash}원"
        )

    def refund(self) -> None:
        change = self.controller.refund_cash()
        msg = "\n".join([f"{k}원: {v}개" for k, v in change.items()])
        messagebox.showinfo("거스름돈 반환", msg or "반환할 금액이 없습니다.")
        # Update the cash label to show that all inserted cash was returned
        self.cash_label.config(text="0원")

    def use_card(self) -> None:
        if self.controller.card.accept():
            self.card_status.config(text="카드 상태: 승인 완료")
            messagebox.showinfo("카드 결제", "결제가 승인되었습니다.")
        else:
            self.card_status.config(text="카드 상태: 결제 실패")

    def select_drink(self, drink: Drink) -> None:
        result = self.controller.dispense(drink)
        messagebox.showinfo("음료 선택", result)
        self.refresh_gui()

    def admin_menu(self) -> None:
        messagebox.showinfo("관리자 모드", "관리자 메뉴로 진입합니다. (구현 예정)")

    def load_image(self, path: str, size=(70, 70)) -> ImageTk.PhotoImage:
        """Load and resize the given image path safely."""
        if not os.path.exists(path):
            img = Image.new("RGB", size, color="gray")
        else:
            img = Image.open(path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
