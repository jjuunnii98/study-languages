"""
Day 14: Python OOP - Attributes & Methods (Professional Version)

This file focuses on:
- instance vs class attributes
- methods that operate on object state
- basic validation and encapsulation using properties
- safe mutation patterns for real-world code

이 파일은 객체의 "상태(state)"를 구성하는 속성(attributes)과
그 상태를 다루는 메서드(methods)를 더 실무적인 관점에서 정리한다.

핵심 포인트:
- 인스턴스 속성 vs 클래스 속성 구분
- 객체 상태 변경 메서드 설계(검증/방어 코드)
- property를 활용한 캡슐화(초입)
"""

from __future__ import annotations

from typing import ClassVar


# ---------------------------------------------------------
# 1) Instance attributes vs Class attributes
# ---------------------------------------------------------
class Account:
    """
    A minimal bank-like account model.

    한국어 설명:
    - 실무 OOP에서 가장 중요한 것은 "상태 + 동작"을 한 객체에 묶는 것
    - Account는 balance(상태)와 deposit/withdraw(행동)을 함께 갖는다
    """

    # Class attribute (shared across all instances)
    # 모든 인스턴스가 공유하는 클래스 속성
    currency: ClassVar[str] = "KRW"

    def __init__(self, owner: str, balance: int = 0) -> None:
        # instance attributes (unique per instance)
        # 각 객체마다 다른 값을 가지는 인스턴스 속성
        self.owner = owner
        self._balance = 0  # 캡슐화를 위해 내부 변수로 관리
        self.balance = balance  # property를 통해 초기값 검증

    # ---------------------------------------------------------
    # 2) Encapsulation via property (초기 캡슐화)
    # ---------------------------------------------------------
    @property
    def balance(self) -> int:
        """Current balance (read-only interface)."""
        return self._balance

    @balance.setter
    def balance(self, value: int) -> None:
        """
        Validate balance assignment.

        한국어 설명:
        - balance는 "음수 불가" 같은 정책이 있을 수 있음
        - property setter에서 규칙을 강제하면, 객체 일관성이 좋아진다
        """
        if not isinstance(value, int):
            raise TypeError("balance must be an integer")
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

    # ---------------------------------------------------------
    # 3) Methods operate on object state
    # ---------------------------------------------------------
    def deposit(self, amount: int) -> None:
        """
        Deposit money into the account.

        한국어 설명:
        - amount 검증(타입/양수 여부)을 통해 방어적 코딩
        - 성공하면 객체 상태(balance)가 변경됨
        """
        self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount: int) -> None:
        """
        Withdraw money from the account.

        한국어 설명:
        - 잔고 부족 체크는 도메인 규칙(비즈니스 로직)에 해당
        - 실패 시 예외로 명확히 알린다
        """
        self._validate_amount(amount)
        if self._balance < amount:
            raise ValueError("insufficient balance")
        self._balance -= amount

    def summary(self) -> str:
        """
        Return a human-readable summary.

        한국어 설명:
        - 상태를 문자열로 표현하는 메서드는 디버깅/로그/리포트에 유용
        """
        return f"Account(owner={self.owner}, balance={self.balance} {self.currency})"

    # ---------------------------------------------------------
    # 4) Private helper method (internal utilities)
    # ---------------------------------------------------------
    def _validate_amount(self, amount: int) -> None:
        """
        Validate deposit/withdraw amount.

        한국어 설명:
        - 반복되는 검증 로직은 private helper로 분리하는 것이 좋다
        - '_' prefix는 내부용(외부에서 직접 호출 비권장) 관례
        """
        if not isinstance(amount, int):
            raise TypeError("amount must be an integer")
        if amount <= 0:
            raise ValueError("amount must be positive")


# ---------------------------------------------------------
# 5) Demonstration (usage examples)
# ---------------------------------------------------------
if __name__ == "__main__":
    # 인스턴스 생성
    acc = Account(owner="Junyeong", balance=1000)
    print(acc.summary())

    # 입금/출금
    acc.deposit(500)
    print("[after deposit] ", acc.summary())

    acc.withdraw(300)
    print("[after withdraw]", acc.summary())

    # 클래스 속성 확인(모든 인스턴스에 공유)
    acc2 = Account(owner="Alice", balance=200)
    print("acc2 currency:", acc2.currency)

    # 정책 강제 확인: 음수 잔고 불가
    try:
        acc.balance = -10
    except Exception as e:
        print("Expected error:", type(e).__name__, "-", e)

    # 정책 강제 확인: 잘못된 amount
    try:
        acc.deposit(-1)
    except Exception as e:
        print("Expected error:", type(e).__name__, "-", e)

"""
Day 14 요약 (OOP)

- 인스턴스 속성: 객체마다 고유한 상태(owner, balance 등)
- 클래스 속성: 모든 객체가 공유하는 값(currency 등)
- 메서드: 객체 상태를 변경/조회하는 행동(입금/출금/요약)
- property: 상태 변경 시 규칙을 강제(캡슐화 초입)
- helper 메서드: 반복 검증 로직을 내부 메서드로 분리

다음 단계:
- __init__과 __repr__/__str__로 객체 표현 강화
- 상속/합성으로 구조 설계 확장
"""