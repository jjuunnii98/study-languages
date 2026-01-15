"""
Day 18: Encapsulation (OOP)

Encapsulation is the practice of bundling data (state) and behavior (methods)
together, while controlling access to the internal state to prevent misuse.

In Python, encapsulation is achieved by:
- A clear public API (methods/properties intended for use)
- Protected-by-convention attributes (single underscore: _attr)
- Name-mangled "private" attributes (double underscore: __attr)
- Properties (@property) to validate and control read/write access

본 파일은 캡슐화(Encapsulation)를 실전 설계 관점에서 다룬다.
캡슐화의 목표는:
- 객체 내부 상태를 외부로부터 보호하고
- 무결성(invariants)을 유지하며
- 안전하고 예측 가능한 인터페이스(API)를 제공하는 것이다.
"""

from __future__ import annotations


# ==================================================
# 1) Encapsulation via Public API + Protected Convention
# ==================================================
class BankAccount:
    """
    A simple bank account that demonstrates encapsulation.

    - balance is kept as a "protected" attribute: _balance
      (single underscore means: "internal use by convention")
    - All changes to balance go through deposit/withdraw methods
      to enforce rules and invariants.

    은행 계좌 예제를 통해 캡슐화의 핵심을 보여준다.
    - _balance는 내부 상태(관례적 보호)
    - 입금/출금 메서드를 통해서만 상태 변경 (규칙 강제)
    """

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = 0.0
        self.deposit(initial_balance)  # 초기값도 동일 규칙을 적용

    @property
    def balance(self) -> float:
        """Read-only access to balance from outside."""
        return self._balance

    def deposit(self, amount: float) -> None:
        """Deposit money, enforcing domain rules."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += float(amount)

    def withdraw(self, amount: float) -> None:
        """Withdraw money, enforcing domain rules."""
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= float(amount)

    def __repr__(self) -> str:
        return f"BankAccount(owner='{self.owner}', balance={self._balance:.2f})"


acc = BankAccount("Junyeong", 100)
acc.deposit(50)
acc.withdraw(30)
print("[account]", acc)
print("[balance read-only]", acc.balance)

# ⚠️ 관례적으로는 외부에서 _balance에 직접 접근하지 않는 것이 원칙
# acc._balance = -999  # 이런 식으로 무결성이 깨질 수 있음 (권장하지 않음)


# ==================================================
# 2) Stronger Encapsulation using Name Mangling (__attr)
# ==================================================
class SecureAccount:
    """
    Demonstrates name-mangled 'private' attribute via __balance.

    - __balance is name-mangled by Python (e.g., _SecureAccount__balance)
    - This discourages accidental access and reduces misuse
    - Not true security, but strong signal + avoids accidental override

    __balance는 '완전한 보안'이 아니라,
    실수 방지(우발적 접근/오버라이딩 방지)를 위한 강한 캡슐화 수단이다.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0) -> None:
        self.owner = owner
        self.__balance = 0.0
        self.deposit(initial_balance)

    @property
    def balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += float(amount)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= float(amount)

    def __repr__(self) -> str:
        return f"SecureAccount(owner='{self.owner}', balance={self.__balance:.2f})"


sec = SecureAccount("Junyeong", 200)
sec.deposit(100)
print("[secure]", sec)

# 아래는 일반 접근이 막힌다(속성 에러가 나거나 접근이 어렵다)
# print(sec.__balance)  # AttributeError

# 하지만 Python은 완전한 private를 강제하지 않는다.
# 원하면 아래처럼 접근 가능하긴 하다(권장하지 않음)
# print(sec._SecureAccount__balance)


# ==================================================
# 3) Encapsulation with Validation using @property setters
# ==================================================
class UserProfile:
    """
    Encapsulation example where properties enforce validation rules.

    - email must contain "@"
    - age must be within a valid range
    - internal state stored as protected attrs (_email, _age)

    @property를 통해 "읽기/쓰기 규칙"을 강제하는 대표 패턴.
    """

    def __init__(self, username: str, email: str, age: int) -> None:
        self.username = username
        self.email = email  # property setter 호출
        self.age = age      # property setter 호출

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("Invalid email: must contain '@'.")
        self._email = value.strip().lower()

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Age must be an integer.")
        if value < 0 or value > 120:
            raise ValueError("Age must be between 0 and 120.")
        self._age = value

    def __repr__(self) -> str:
        return f"UserProfile(username='{self.username}', email='{self.email}', age={self.age})"


profile = UserProfile("junyeong", "JJUUNNII98@yonsei.ac.kr", 27)
print("[profile]", profile)


# ==================================================
# 4) Practical Encapsulation: Small Domain Model (Transaction Log)
# ==================================================
class TransactionalAccount:
    """
    A more practical account model:
    - Encapsulates balance changes
    - Keeps an internal transaction log
    - Exposes transaction history as a read-only copy

    실무에서는 내부 상태뿐만 아니라 "내부 기록"도 캡슐화 대상이다.
    내부 list를 그대로 반환하면 외부에서 임의 수정 가능하므로,
    복사본을 제공하는 패턴이 자주 사용된다.
    """

    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.__balance = 0.0
        self.__transactions: list[tuple[str, float]] = []  # (type, amount)

    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def transactions(self) -> list[tuple[str, float]]:
        """Return a defensive copy to prevent external mutation."""
        return list(self.__transactions)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.__balance += float(amount)
        self.__transactions.append(("DEPOSIT", float(amount)))

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")
        if amount > self.__balance:
            raise ValueError("Insufficient funds.")
        self.__balance -= float(amount)
        self.__transactions.append(("WITHDRAW", float(amount)))

    def __repr__(self) -> str:
        return f"TransactionalAccount(owner='{self.owner}', balance={self.__balance:.2f}, tx_count={len(self.__transactions)})"


tx_acc = TransactionalAccount("Junyeong")
tx_acc.deposit(100)
tx_acc.withdraw(40)

print("[tx account]", tx_acc)
print("[tx history copy]", tx_acc.transactions)

# 외부에서 transactions 리스트를 수정해도 내부에는 영향 없음 (방어적 복사)
external = tx_acc.transactions
external.append(("HACK", 999))
print("[external modified]", external)
print("[internal remains]", tx_acc.transactions)


# ==================================================
# Summary (요약)
# ==================================================
# 1) 캡슐화는 "상태 보호 + 규칙 강제 + 안정적 인터페이스 제공"을 의미한다.
# 2) Python에서는:
#    - _attr: 관례적 보호 (protected)
#    - __attr: name mangling 기반 강한 캡슐화 (private-like)
#    - @property: 검증/제어 가능한 public API 제공
# 3) 실무에서는 내부 상태뿐 아니라 내부 컬렉션/로그도 보호해야 한다.