"""
Day (Core): Error Handling in Python

This file covers practical error handling patterns in Python:
- try / except / else / finally
- catching specific exceptions
- raising custom exceptions
- defensive coding and validation
- logging-friendly error messages

본 파일은 파이썬에서 "예외 처리(Exception Handling)"를 다룬다.
실무/연구 코드에서 안정성과 재현성을 높이기 위해
예외 처리는 필수 역량이다.

핵심 목표:
- 오류가 발생해도 프로그램이 안전하게 동작하도록 만들기
- 원인 분석이 가능한 메시지와 구조를 남기기
- 입력 검증과 방어적 코딩(defensive coding) 습관화
"""

from __future__ import annotations

from typing import Any


# ---------------------------------------------------------
# 1. Basic try / except
# ---------------------------------------------------------
# try 블록 안에서 오류가 발생하면,
# except 블록이 실행되며 프로그램이 강제 종료되지 않는다.

print("\n[1] Basic try/except")

try:
    result = 10 / 0
    print("result:", result)
except ZeroDivisionError:
    print("Error: Division by zero is not allowed. (0으로 나눌 수 없습니다.)")


# ---------------------------------------------------------
# 2. Catching specific exceptions (구체적인 예외 잡기)
# ---------------------------------------------------------
# 실무에서는 가능한 한 "구체적인 예외"를 잡는 것이 좋다.
# (모든 예외를 다 잡는 except Exception은 디버깅을 어렵게 만들 수 있음)

print("\n[2] Specific exceptions")

def safe_int(value: Any) -> int:
    """
    Convert value to int safely.

    Parameters
    ----------
    value : Any
        Input value to convert

    Returns
    -------
    int
        Converted integer

    Raises
    ------
    ValueError
        If conversion fails
    """
    try:
        return int(value)
    except (TypeError, ValueError) as e:
        # 한국어 해설:
        # - TypeError: int(None) 같은 경우
        # - ValueError: int("abc") 같은 경우
        raise ValueError(f"Cannot convert to int: {value!r}") from e


for v in ["123", 45.6, None, "abc"]:
    try:
        print(v, "->", safe_int(v))
    except ValueError as e:
        print("Conversion failed:", e)


# ---------------------------------------------------------
# 3. try / except / else / finally
# ---------------------------------------------------------
# else: try에서 예외가 없을 때만 실행
# finally: 예외 발생 여부와 관계없이 항상 실행 (정리 작업에 유용)

print("\n[3] else/finally pattern")

def divide(a: float, b: float) -> float:
    """
    Divide a by b with safe handling.
    """
    try:
        q = a / b
    except ZeroDivisionError:
        print("Error: b is zero. Returning infinity-like value.")
        return float("inf")
    else:
        # 예외가 없을 때만 실행
        return q
    finally:
        # 항상 실행: 로그/리소스 정리 등에 사용
        print(f"divide() called with a={a}, b={b}")


print("10/2 =", divide(10, 2))
print("10/0 =", divide(10, 0))


# ---------------------------------------------------------
# 4. Validation (입력 검증) = 오류 예방의 핵심
# ---------------------------------------------------------
# 예외 처리는 '사후 처리'이지만,
# 입력 검증은 오류 자체를 예방한다.

print("\n[4] Input validation")

def mean(values: list[float]) -> float:
    """
    Compute mean of a list of floats.

    Defensive rules:
    - values must be non-empty
    - all items must be numeric (float or int)
    """
    if not values:
        raise ValueError("values must not be empty (빈 리스트는 평균을 계산할 수 없음)")

    total = 0.0
    for x in values:
        if not isinstance(x, (int, float)):
            raise TypeError(f"Non-numeric value found: {x!r}")
        total += float(x)

    return total / len(values)


try:
    print("mean([1,2,3]) =", mean([1, 2, 3]))
    print("mean([]) =", mean([]))
except Exception as e:
    print("Validation error:", e)


# ---------------------------------------------------------
# 5. Raising exceptions intentionally (의도적으로 예외 발생)
# ---------------------------------------------------------
# 실무에서는 "조용히 실패"하는 것보다
# "명확하게 실패"하는 것이 더 안전하다.

print("\n[5] Raising exceptions")

def withdraw(balance: int, amount: int) -> int:
    """
    Withdraw amount from balance.

    Raises ValueError if amount is invalid.
    """
    if amount <= 0:
        raise ValueError("amount must be positive (출금 금액은 양수여야 함)")
    if amount > balance:
        raise ValueError("insufficient funds (잔액 부족)")
    return balance - amount


try:
    print("new balance:", withdraw(100, 30))
    print("new balance:", withdraw(100, 200))
except ValueError as e:
    print("Withdraw error:", e)


# ---------------------------------------------------------
# 6. Custom exceptions (사용자 정의 예외)
# ---------------------------------------------------------
# 특정 도메인의 오류를 더 명확히 표현하고 싶을 때 사용
# (예: 데이터 파이프라인, 모델 학습, 서비스 로직 등)

print("\n[6] Custom exception")

class DataValidationError(Exception):
    """Raised when dataset validation fails."""
    pass


def validate_schema(row: dict[str, Any], required_keys: list[str]) -> None:
    """
    Validate that row contains all required keys.

    Raises DataValidationError if missing keys exist.
    """
    missing = [k for k in required_keys if k not in row]
    if missing:
        raise DataValidationError(f"Missing keys: {missing}")


sample_row = {"id": 1, "name": "Junyeong"}
try:
    validate_schema(sample_row, ["id", "name", "age"])
except DataValidationError as e:
    print("Schema error:", e)


# ---------------------------------------------------------
# 7. Practical pattern: safe parsing with fallback
# ---------------------------------------------------------
# 실무/분석에서 흔한 패턴:
# - 파싱을 시도하고
# - 실패하면 기본값을 주거나 None 처리
# - 실패 횟수/원인을 로그로 남길 수 있게 구성

print("\n[7] Safe parsing pattern")

def parse_float(value: Any, default: float | None = None) -> float | None:
    """
    Try to parse float; return default if fails.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


raw = ["3.14", "10", None, "abc", ""]
parsed = [parse_float(x, default=None) for x in raw]
print("raw   :", raw)
print("parsed:", parsed)


# ---------------------------------------------------------
# 8. Summary
# ---------------------------------------------------------
"""
Day (Core) 요약 (한국어)

- try/except로 오류를 안전하게 처리할 수 있다
- 가능한 한 구체적인 예외(ZeroDivisionError 등)를 잡는 것이 좋다
- else/finally 패턴은 성공/정리 로직을 분리하는 데 유용하다
- 입력 검증은 오류를 예방하는 가장 강력한 방법이다
- raise로 '명확한 실패'를 만들면 디버깅/품질 관리가 쉬워진다
- 사용자 정의 예외는 도메인 오류를 명확히 표현한다
- 실무에서는 파싱 실패에 대한 fallback(default/None) 패턴이 자주 사용된다
"""