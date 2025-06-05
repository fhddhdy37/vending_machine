import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from .controller import Controller
from .drink import Drink


class Machine:
    """자판기의 GUI 동작을 담당하는 클래스.

    ``root``에 배치된 GUI 요소를 관리하며 ``controller``를 통해 비즈니스 로직을
    수행한다. ``images``와 ``buttons`` 리스트는 동적으로 생성된 위젯과 이미지를
    보관한다.
    """

    def __init__(self, root: tk.Tk) -> None:
        """GUI를 초기화하고 컨트롤러를 생성한다.

        Parameters
        ----------
        root : :class:`tk.Tk`
            최상위 윈도우 객체로, 자판기 화면이 표시될 대상이다.

        ``controller``를 생성하고 ``images``와 ``buttons`` 리스트를 준비한다.
        """
        self.root = root
        self.controller = Controller()
        self.root.title("자판기 시스템")
        # adjust window size as requested
        self.root.geometry("948x431")
        self.root.configure(bg="black")
        self.images: list[ImageTk.PhotoImage] = []
        self.buttons: list[tk.Widget] = []
        self.build_frame()

    def build_frame(self) -> None:
        """버튼과 화면 요소를 생성하여 GUI를 구성한다.

        ``controller.drinks`` 정보를 사용하여 음료 버튼을 만들고 ``buttons``와
        ``images`` 리스트에 저장한다. 금액 표시용 ``cash_label``과 각종 제어
        위젯들도 이 단계에서 생성된다.
        """
        # 카드 처리 중 위젯 제어를 쉽게 하기 위해 목록을 관리
        self.buttons.clear()

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
                    self.buttons.append(btn)

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
        self.cash_menu = tk.OptionMenu(control_panel, self.cash_var, 1000, 500, 100, 50)
        self.cash_menu.grid(row=0, column=0)
        self.buttons.append(self.cash_menu)

        self.insert_button = tk.Button(
            control_panel,
            text="투입",
            bg="green",
            fg="white",
            command=self.insert_cash,
        )
        self.insert_button.grid(row=0, column=1, padx=5)
        self.buttons.append(self.insert_button)

        self.refund_button = tk.Button(
            control_panel,
            text="반환",
            bg="red",
            fg="white",
            command=self.refund,
        )
        self.refund_button.grid(row=0, column=2, padx=5)
        self.buttons.append(self.refund_button)

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

        self.card_button = tk.Button(
            entry_button_frame,
            text="카드 투입",
            bg="green",
            fg="white",
            command=self.use_card,
        )
        self.card_button.pack(side="left", padx=5)
        self.buttons.append(self.card_button)

        # Use a keyhole image for the admin button and place it at the
        # bottom-right corner of the admin panel
        admin_img = self.load_image("src/drinks/keyhole.png", (15, 15))
        admin_btn = tk.Button(admin_panel, image=admin_img, command=self.admin_menu, bg="white")
        self.images.append(admin_img)
        admin_btn.place(relx=1.0, rely=1.0, anchor="se")
        self.buttons.append(admin_btn)

    def refresh_gui(self) -> None:
        """화면을 초기화하고 다시 그린다.

        ``root`` 하위의 모든 위젯을 제거한 뒤 :py:meth:`build_frame`을
        호출하여 최신 상태를 반영한다.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_frame()

    def disable_widgets(self) -> None:
        """카드 결제 처리 중에는 모든 위젯을 비활성화한다.

        ``buttons`` 리스트에 저장된 위젯과 ``card_entry`` 입력창의 ``state`` 값을
        변경하여 사용자가 조작할 수 없도록 한다.
        """
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.card_entry.config(state=tk.DISABLED)

    def enable_widgets(self) -> None:
        """카드 결제 완료 후 모든 위젯을 다시 활성화한다.

        ``disable_widgets``에서 비활성화한 위젯들의 ``state``를 되돌린다.
        """
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)
        self.card_entry.config(state=tk.NORMAL)

    def insert_cash(self) -> None:
        """투입된 금액을 컨트롤러에 전달한다.

        ``cash_var``에 설정된 화폐 단위를 ``controller.input_cash``에 전달하여
        ``inserted_cash`` 값을 증가시키고, ``cash_label``에 즉시 반영한다.
        """
        amount = self.cash_var.get()
        self.controller.input_cash({amount: 1})
        # Update only the cash label instead of rebuilding the entire GUI
        self.cash_label.config(
            text=f"{self.controller.inserted_cash}원"
        )

    def refund(self) -> None:
        """투입된 금액을 환불하고 거스름돈을 표시한다.

        ``controller.refund_cash``로 계산된 거스름돈을 메시지 박스로 보여주고
        ``cash_label``을 0원으로 갱신한다.
        """
        change = self.controller.refund_cash()
        msg = "\n".join([f"{k}원: {v}개" for k, v in change.items()])
        messagebox.showinfo("거스름돈 반환", msg or "반환할 금액이 없습니다.")
        # Update the cash label to show that all inserted cash was returned
        self.cash_label.config(text="0원")

    def use_card(self) -> None:
        """카드 번호를 입력받아 카드 삽입을 시도한다.

        ``card_entry``에서 번호를 읽어 ``controller.card.insert_card``를 호출한
        뒤 결과에 따라 ``card_status`` 라벨을 갱신한다.
        """
        number = self.card_entry.get()
        if not number:
            messagebox.showwarning("카드 투입", "카드 번호를 입력해주세요.")
            return
        if self.controller.card.insert_card(number):
            self.card_status.config(text="카드 상태: 결제 대기중")
        else:
            messagebox.showerror("카드 오류", "유효하지 않은 카드")

    def select_drink(self, drink: Drink) -> None:
        """음료 버튼 클릭 시 결제 여부를 판단하여 제공한다.

        Parameters
        ----------
        drink : :class:`Drink`
            선택된 음료 객체.

        카드가 삽입되어 있으면 ``complete_card_payment``를 예약하고, 그렇지
        않으면 ``controller.dispense`` 결과를 메시지로 출력한다.
        """
        # 카드가 삽입되었다면 먼저 카드 결제를 진행
        if self.controller.card.inserted and not self.controller.card.status:
            if drink.count <= 0:
                messagebox.showinfo("음료 선택", "재고 없음")
                return
            self.card_status.config(text="카드 상태: 결제 요청중")
            self.disable_widgets()
            # After 2 seconds approve the card and dispense the drink
            self.root.after(2000, lambda d=drink: self.complete_card_payment(d))
        else:
            result = self.controller.dispense(drink)
            messagebox.showinfo("음료 선택", result)
            self.refresh_gui()

    def complete_card_payment(self, drink: Drink) -> None:
        """승인 지연 후 카드 결제를 마무리한다.

        Parameters
        ----------
        drink : :class:`Drink`
            결제를 시도한 음료 객체.

        ``controller.card``의 상태를 승인으로 변경한 뒤 ``dispense``를 호출하고
        UI 요소를 원래대로 복구한다.
        """
        self.controller.card.approve()
        result = self.controller.dispense(drink)
        self.card_status.config(text="카드 상태: 승인 완료")
        messagebox.showinfo("카드 결제", "결제가 완료되었습니다")
        if result:
            # Update inventory display
            self.refresh_gui()
        # reset card for next transaction
        self.controller.card.reset()
        self.card_entry.delete(0, tk.END)
        self.enable_widgets()

    def admin_menu(self) -> None:
        """관리자용 현금 및 재고 관리 창을 연다.

        ``cashes``와 ``drinks`` 값을 조정할 수 있는 별도 창을 생성하여 보여주며
        창이 닫힐 때 ``apply_changes`` 내부 함수로 변경 사항을 반영한다.
        """
        self.disable_widgets()
        window = tk.Toplevel(self.root)
        window.title("관리자 메뉴")

        # 창을 닫을 때 호출되는 내부 함수
        def on_close() -> None:
            apply_changes()
            self.enable_widgets()
            window.destroy()

        window.protocol("WM_DELETE_WINDOW", on_close)

        cash_vars: dict[int, tk.IntVar] = {}
        # use a list for drink variables to avoid hashing Drink instances
        drink_vars: list[tk.IntVar] = []
        price_vars: list[tk.IntVar] = []

        cash_frame = tk.LabelFrame(window, text="현금 시재 관리")
        cash_frame.pack(fill="x", padx=10, pady=5)

        for idx, currency in enumerate(sorted(self.controller.cashes.keys(), reverse=True)):
            tk.Label(cash_frame, text=f"{currency}원").grid(row=idx, column=0, padx=5, pady=2)
            var = tk.IntVar(value=self.controller.cashes[currency])
            tk.Entry(cash_frame, width=5, textvariable=var).grid(row=idx, column=1, padx=5, pady=2)
            cash_vars[currency] = var

        drink_frame = tk.LabelFrame(window, text="음료 재고 관리")
        drink_frame.pack(fill="both", expand=True, padx=10, pady=5)

        admin_images: list[ImageTk.PhotoImage] = []

        for i in range(4):
            for j in range(6):
                idx = i * 6 + j
                if idx >= len(self.controller.drinks):
                    continue
                drink = self.controller.drinks[idx]
                cell = tk.Frame(drink_frame)
                cell.grid(row=i, column=j, padx=5, pady=5)
                img = self.load_image(drink.image_path, (40, 40))
                tk.Label(cell, image=img).pack()
                admin_images.append(img)
                tk.Label(cell, text=drink.name).pack()
                var = tk.IntVar(value=drink.count)
                tk.Entry(cell, width=5, textvariable=var).pack()
                drink_vars.append(var)
                price_var = tk.IntVar(value=drink.price)
                tk.Entry(cell, width=5, textvariable=price_var).pack()
                price_vars.append(price_var)

        # 입력된 값을 실제 데이터에 반영하는 내부 함수
        def apply_changes() -> None:
            for currency, var in cash_vars.items():
                self.controller.cashes[currency] = max(0, var.get())
            for drink, c_var, p_var in zip(self.controller.drinks, drink_vars, price_vars):
                drink.count = max(0, c_var.get())
                drink.price = max(0, p_var.get())
            self.refresh_gui()

        tk.Button(window, text="저장", command=apply_changes).pack(pady=5)
        tk.Button(window, text="닫기", command=on_close).pack(pady=5)

    def load_image(self, path: str, size=(70, 70)) -> ImageTk.PhotoImage:
        """이미지 파일을 로드하고 지정 크기로 변환한다.

        Parameters
        ----------
        path : str
            이미지 파일 경로.
        size : tuple[int, int], optional
            불러올 이미지의 크기. 기본값은 ``(70, 70)``.

        경로가 없으면 회색 이미지로 대체하고, ``images`` 목록에 저장되지 않은
        새 :class:`ImageTk.PhotoImage` 객체를 반환한다.
        """
        if not os.path.exists(path):
            img = Image.new("RGB", size, color="gray")
        else:
            img = Image.open(path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
