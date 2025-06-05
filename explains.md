# 클래스별 변수 및 함수 설명

## `Machine`
| 이름                                            | 설명                                                       |
| --------------------------------------------- | -------------------------------------------------------- |
| **속성**                                        |                                                          |
| `root`                                        | Tkinter 최상위 윈도우.                                         |
| `controller`                                  | 비즈니스 로직을 담당하는 `Controller` 인스턴스.                         |
| `images`, `buttons`                           | 동적으로 생성된 이미지 및 버튼 위젯을 저장하는 리스트.                          |
| `cash_label`                                  | 현재 투입된 금액 표시용 라벨.                                        |
| `cash_var`                                    | 현금 선택 메뉴(`OptionMenu`)와 연결된 `IntVar`.                    |
| `cash_menu`, `insert_button`, `refund_button` | 현금 투입과 반환 기능을 담당하는 위젯.                                   |
| `card_status`, `card_entry`, `card_button`    | 카드 상태 표시 및 카드 번호 입력을 위한 위젯.                              |
| **메서드**                                       |                                                          |
| `__init__(root)`                              | GUI 초기화 후 기본 프레임을 구성.                                    |
| `build_frame()`                               | 음료 버튼, 금액 표시, 현금·카드 제어 위젯 등을 생성.                         |
| `refresh_gui()`                               | 모든 위젯을 파괴 후 `build_frame`으로 다시 그림.                       |
| `disable_widgets()/enable_widgets()`          | 카드 결제 중 사용자 입력을 차단하거나 다시 활성화.                            |
| `insert_cash()`                               | 선택한 화폐 단위를 `controller.input_cash`에 전달하고 금액 라벨 갱신.       |
| `refund()`                                    | `controller.refund_cash` 결과를 메시지로 보여주고 금액 라벨 초기화.        |
| `use_card()`                                  | 입력된 카드 번호를 `controller.card.insert_card`에 전달하여 카드 삽입 시도. |
| `select_drink(drink)`                         | 음료 버튼 클릭 시 현금 또는 카드 결제 여부를 확인 후 `dispense` 호출.           |
| `complete_card_payment(drink)`                | 일정 시간 지연 후 카드 승인 → 음료 제공 과정을 마무리.                        |
| `admin_menu()`                                | 관리자용 팝업 창을 띄워 현금 시재와 음료 재고/가격을 수정 가능.                    |
| `load_image(path, size=(70,70))`              | 이미지 파일을 로드 후 크기 조정하여 `ImageTk.PhotoImage` 객체 반환.         |

## `Controller`
| 이름                                    | 설명                                                                     |
| ------------------------------------- | ---------------------------------------------------------------------- |
| **속성**                                |                                                                        |
| `cashes: Dict[int, int]`              | 화폐 단위별 시재. 1000/500/100/50원을 기본으로 보유.                                  |
| `drinks: List[Drink]`                 | 자판기에 등록된 음료 목록.                                                        |
| `card: Card`                          | 카드 결제 모듈.                                                              |
| `inserted_cash: int`                  | 사용자가 투입한 총 현금액.                                                        |
| **메서드**                               |                                                                        |
| `input_cash(amounts: Dict[int, int])` | `{화폐단위: 개수}` 형식의 금액을 투입하여 시재와 `inserted_cash`를 갱신.                     |
| `refund_cash() -> Dict[int, int]`     | `inserted_cash`만큼 거스름돈을 계산하여 화폐 단위별 개수로 반환 후 `inserted_cash`를 0으로 초기화. |
| `add_drinks(drink: Drink)`            | 음료 객체를 `drinks` 리스트에 추가.                                               |
| `dispense(drink: Drink) -> str`       | 투입 금액 또는 카드 승인 여부를 확인하여 재고를 차감하고 결과 문자열 반환.                            |

## `Card`
| 이름                                 | 설명                                                                |
| ---------------------------------- | ----------------------------------------------------------------- |
| **속성**                             |                                                                   |
| `status`                           | 결제 승인 여부를 나타내는 bool 값.                                            |
| `inserted`                         | 카드가 삽입된 상태인지 여부.                                                  |
| `number`                           | 삽입된 카드 번호.                                                        |
| **메서드**                            |                                                                   |
| `insert_card(number: str) -> bool` | 10자리 영문/숫자 카드 번호가 사전 등록 목록에 존재하면 `inserted=True`로 설정하고 `True` 반환. |
| `approve()`                        | 결제를 승인하여 `status=True`로 변경.                                       |
| `reset()`                          | 거래 종료 후 `number`, `status`, `inserted` 값을 초기화.                    |
| `accept() -> bool`                 | 내부적으로 `approve()`를 호출 후 `status` 값을 반환.                           |

## `Drink`
| 속성                                 | 설명                                                                |
| ---------------------------------- | ----------------------------------------------------------------- |
| `name`                           | 음료명                                            |
| `price`                         | 음료 가격                                                  |
| `count`                           | 음료 재고                                                        |