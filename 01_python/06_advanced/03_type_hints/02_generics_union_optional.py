"""
============================================================
Day 79 — Python Type Hints: Generics, Union, Optional
File: 01_python/06_advanced/03_type_hints/02_generics_union_optional.py

목표
- Generic, Union, Optional의 개념을 이해한다.
- 재사용 가능한 타입 안전 코드 작성 방법을 익힌다.
- 여러 타입을 허용하거나, 값이 없을 수 있는 상황을 명확히 표현한다.
- 실무에서 자주 쓰는 타입 힌트 패턴을 연습한다.

핵심 개념
1) Generic
   - 특정 타입 하나에 묶이지 않고, 여러 타입에 재사용 가능한 구조를 만든다.

2) Union
   - 둘 이상의 타입을 허용한다.

3) Optional
   - 값이 특정 타입이거나 None일 수 있음을 나타낸다.
   - Optional[T] == Union[T, None]

한국어 설명
이번 파일은 "타입 힌트를 더 유연하게 사용하는 방법"을 다룬다.

기본 타입 힌트가
"이 변수는 int다"
수준이라면,

이번 단계는
"이 함수는 어떤 타입이든 받을 수 있다"
"이 값은 int 또는 str일 수 있다"
"이 값은 없을 수도 있다"
같은 상황을 표현하는 것이다.

이 개념은 실무에서 매우 자주 사용된다.
============================================================
"""

from __future__ import annotations

from typing import Dict, Generic, List, Optional, Tuple, TypeVar, Union


# ------------------------------------------------------------
# 1) TypeVar: Generic의 기본 재료
# ------------------------------------------------------------
# 한국어 설명
# TypeVar는 "아직 정해지지 않은 타입"을 나타낸다.
# 아래 T는 나중에 int, str, float 등으로 대체될 수 있다.
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


# ------------------------------------------------------------
# 2) Generic Function Example
# ------------------------------------------------------------
# 한국어 설명
# 입력 리스트의 첫 번째 값을 반환하는 함수
# 어떤 타입의 리스트든 재사용 가능하다.
def get_first_item(items: List[T]) -> T:
    return items[0]


first_int: int = get_first_item([10, 20, 30])
first_str: str = get_first_item(["btc", "eth", "xrp"])

print("First int:", first_int)
print("First str:", first_str)


# ------------------------------------------------------------
# 3) Generic Function: Last Item
# ------------------------------------------------------------
def get_last_item(items: List[T]) -> T:
    return items[-1]


last_float: float = get_last_item([1.5, 2.3, 3.9])
last_symbol: str = get_last_item(["SOL", "DOGE", "ADA"])

print("Last float:", last_float)
print("Last symbol:", last_symbol)


# ------------------------------------------------------------
# 4) Generic Pair Function
# ------------------------------------------------------------
# 한국어 설명
# 두 값을 튜플로 묶어서 반환
# 서로 다른 타입 조합도 가능하다.
def make_pair(left: K, right: V) -> Tuple[K, V]:
    return left, right


pair1: Tuple[str, int] = make_pair("BTC", 100)
pair2: Tuple[int, float] = make_pair(1, 3.14)

print("Pair 1:", pair1)
print("Pair 2:", pair2)


# ------------------------------------------------------------
# 5) Generic Class Example
# ------------------------------------------------------------
# 한국어 설명
# Box는 어떤 타입의 값이든 담을 수 있는 제네릭 클래스다.
class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get_value(self) -> T:
        return self.value

    def set_value(self, value: T) -> None:
        self.value = value


int_box = Box
str_box = Box[str]("risk-engine")

print("Int box:", int_box.get_value())
print("Str box:", str_box.get_value())

int_box.set_value(200)
str_box.set_value("crypto-llm")

print("Updated int box:", int_box.get_value())
print("Updated str box:", str_box.get_value())


# ------------------------------------------------------------
# 6) Union Basics
# ------------------------------------------------------------
# 한국어 설명
# int 또는 float를 받아 float로 변환하는 함수
def to_float(value: Union[int, float]) -> float:
    return float(value)


print("Union int to float:", to_float(10))
print("Union float to float:", to_float(10.75))


# ------------------------------------------------------------
# 7) Union with Different Types
# ------------------------------------------------------------
# 한국어 설명
# 문자열 또는 숫자를 받아 문자열로 설명을 반환
def describe_value(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return f"Integer value: {value}"
    return f"String value: {value}"


print(describe_value(42))
print(describe_value("bitcoin"))


# ------------------------------------------------------------
# 8) Optional Basics
# ------------------------------------------------------------
# 한국어 설명
# 사용자를 찾지 못하면 None을 반환할 수 있다.
def find_exchange_name(exchange_id: int) -> Optional[str]:
    if exchange_id == 1:
        return "Upbit"
    if exchange_id == 2:
        return "Binance"
    return None


exchange_1 = find_exchange_name(1)
exchange_99 = find_exchange_name(99)

print("Exchange 1:", exchange_1)
print("Exchange 99:", exchange_99)


# ------------------------------------------------------------
# 9) Optional with Safe Handling
# ------------------------------------------------------------
# 한국어 설명
# Optional 값은 None일 수 있으므로, 바로 쓰지 말고 확인하는 습관이 중요하다.
def print_exchange_message(exchange_name: Optional[str]) -> None:
    if exchange_name is None:
        print("Exchange not found.")
        return

    print(f"Selected exchange: {exchange_name}")


print_exchange_message(exchange_1)
print_exchange_message(exchange_99)


# ------------------------------------------------------------
# 10) Union + Optional Together
# ------------------------------------------------------------
# 한국어 설명
# 숫자/문자열 입력을 받아 파싱하되, 실패하면 None 반환
def parse_score(value: Union[int, str]) -> Optional[float]:
    try:
        return float(value)
    except ValueError:
        return None


parsed_1 = parse_score(88)
parsed_2 = parse_score("91.5")
parsed_3 = parse_score("not-a-number")

print("Parsed 1:", parsed_1)
print("Parsed 2:", parsed_2)
print("Parsed 3:", parsed_3)


# ------------------------------------------------------------
# 11) Generic Dictionary Helper
# ------------------------------------------------------------
# 한국어 설명
# 딕셔너리에서 key에 해당하는 값을 가져오는 제네릭 함수
# 값이 없을 수도 있으므로 Optional[V] 반환
def safe_get(data: Dict[K, V], key: K) -> Optional[V]:
    return data.get(key)


market_prices: Dict[str, float] = {
    "BTC": 102000.5,
    "ETH": 5200.0,
    "XRP": 1.85,
}

btc_price = safe_get(market_prices, "BTC")
sol_price = safe_get(market_prices, "SOL")

print("BTC price:", btc_price)
print("SOL price:", sol_price)


# ------------------------------------------------------------
# 12) Practical Example: Risk Label
# ------------------------------------------------------------
# 한국어 설명
# score는 숫자 또는 문자열일 수 있고,
# 파싱 실패 시 None을 반환할 수 있다.
def classify_risk(score: Union[int, float, str]) -> Optional[str]:
    try:
        numeric_score = float(score)
    except ValueError:
        return None

    if numeric_score >= 80:
        return "HIGH"
    if numeric_score >= 50:
        return "MEDIUM"
    return "LOW"


print("Risk 92:", classify_risk(92))
print("Risk 65.5:", classify_risk(65.5))
print("Risk '45':", classify_risk("45"))
print("Risk 'unknown':", classify_risk("unknown"))


# ------------------------------------------------------------
# 13) Generic Identity Function
# ------------------------------------------------------------
# 한국어 설명
# 입력된 값을 그대로 반환하는 가장 대표적인 Generic 예제
def identity(value: T) -> T:
    return value


print("Identity int:", identity(123))
print("Identity str:", identity("llm"))
print("Identity list:", identity([1, 2, 3]))


# ------------------------------------------------------------
# 14) Summary Output
# ------------------------------------------------------------
print("----- Generics / Union / Optional Summary -----")
print("✔ Generic: 타입 재사용성을 높인다")
print("✔ Union: 여러 타입을 허용한다")
print("✔ Optional: 값이 없을 수도 있음을 표현한다")
print("✔ 실무에서는 API, 데이터 파이프라인, 모델 출력 설계에 자주 쓰인다")
print("------------------------------------------------")