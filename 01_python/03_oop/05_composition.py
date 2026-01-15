"""
Day 17: Inheritance (OOP) — Practical Design Patterns

This file upgrades the inheritance examples to a more professional level:
- safe initialization with super()
- method overriding + extending parent behavior
- designing reusable base classes for data/ML workflows
- using @property for clean interfaces
- a light intro to multiple inheritance (mixin pattern)

본 파일은 상속을 '실전 설계' 관점에서 다룬다:
- super()를 통한 안전한 초기화
- 오버라이딩(재정의) + 부모 기능 확장
- 데이터/ML 파이프라인에서 재사용 가능한 베이스 클래스 설계
- @property를 통한 깔끔한 인터페이스 제공
- (가볍게) 믹스인 기반 다중 상속 패턴 소개
"""

from __future__ import annotations


# --------------------------------------------------
# 1) Base Class + Child Class (기본 상속 구조)
# --------------------------------------------------
class Person:
    """A base class that models a person.

    사람(Person)을 표현하는 기본 클래스.
    """

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def describe(self) -> str:
        """Return a developer-friendly description."""
        return f"Person(name='{self.name}', age={self.age})"


class Student(Person):
    """A derived class that extends Person with 'major'.

    Person을 상속받아 전공(major) 정보를 추가한 Student 클래스.
    """

    def __init__(self, name: str, age: int, major: str) -> None:
        # 부모 초기화 로직 재사용 (안전하고 표준적인 방식)
        super().__init__(name, age)
        self.major = major

    def describe(self) -> str:
        """Override and extend the parent behavior.

        부모 메서드를 '재정의(override)'하면서 내용을 확장한다.
        """
        base = super().describe()
        return f"{base[:-1]}, major='{self.major}')"


s = Student("Junyeong", 27, "Data Science")
print(s.describe())


# --------------------------------------------------
# 2) Why super() Matters (실무 포인트)
# --------------------------------------------------
# - 상속 구조가 커질수록 부모 클래스의 초기화 로직을 누락하면
#   객체가 불완전한 상태가 되어 버그가 발생하기 쉽다.
# - super()는 표준적인 초기화 연결고리 역할을 한다.


# --------------------------------------------------
# 3) A Practical Pattern: Base Class for ML/Analytics
# --------------------------------------------------
# 실전에서는 '공통 인터페이스(계약)'를 제공하는 베이스 클래스를 만들어두면
# 팀 협업과 확장성이 크게 좋아진다.

class BaseModel:
    """A minimal base class that defines an interface for models.

    모델이 반드시 구현해야 하는 메서드(인터페이스)를 정의한다.
    """

    def fit(self, X, y) -> "BaseModel":
        raise NotImplementedError("fit() must be implemented in subclasses")

    def predict(self, X):
        raise NotImplementedError("predict() must be implemented in subclasses")


class LogisticRegressionModel(BaseModel):
    """An example model implementation.

    실제 ML 라이브러리(예: scikit-learn)처럼
    동일한 인터페이스를 가진 모델 객체를 만든다고 생각하면 된다.
    """

    def __init__(self) -> None:
        self.is_fitted = False

    def fit(self, X, y) -> "LogisticRegressionModel":
        # 실제로는 학습 로직이 들어갈 자리
        self.is_fitted = True
        print("[fit] LogisticRegressionModel fitted")
        return self

    def predict(self, X):
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before calling predict()")
        print("[predict] Predicting with LogisticRegressionModel")
        return [0] * len(X)


model = LogisticRegressionModel()
model.fit([1, 2, 3], [0, 1, 0])
print(model.predict([1, 2]))


# --------------------------------------------------
# 4) @property for Cleaner Interfaces (실전 감각)
# --------------------------------------------------
# 내부 구현은 숨기고, 읽기 쉬운 "속성처럼 보이는 메서드"를 제공할 수 있다.

class Account:
    """A simple example showing encapsulation with @property.

    @property로 외부에는 깔끔한 인터페이스를 제공하고,
    내부 데이터는 통제 가능하게 만든다.
    """

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self._balance = float(balance)

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount


acc = Account("Junyeong", 100)
acc.deposit(50)
acc.withdraw(30)
print("[account] balance =", acc.balance)


# --------------------------------------------------
# 5) (Light) Multiple Inheritance via Mixins
# --------------------------------------------------
# 다중 상속은 복잡해질 수 있어 조심해야 한다.
# 하지만 'Mixin' 패턴은 특정 기능을 얇게 추가할 때 유용하다.

class TimestampMixin:
    """A mixin providing a timestamp-like behavior (toy example)."""

    def created_info(self) -> str:
        return "created_at=YYYY-MM-DD (example)"


class AuditedAccount(TimestampMixin, Account):
    """Account + additional capability from TimestampMixin."""

    def audit(self) -> str:
        return f"owner='{self.owner}', balance={self.balance}, {self.created_info()}"


aud = AuditedAccount("Junyeong", 200)
print("[audit]", aud.audit())


# --------------------------------------------------
# Summary
# --------------------------------------------------
# - Inheritance helps reuse code and extend behavior
# - super() is essential for safe initialization and method extension
# - Base classes define interfaces (important in ML/data pipelines)
# - @property makes APIs clean while controlling internal state
# - Mixins are a safe, lightweight form of multiple inheritance