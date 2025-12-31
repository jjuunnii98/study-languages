"""
Day (Core): Advanced Functions

This file covers advanced function patterns in Python:
- Default arguments
- *args and **kwargs
- Argument unpacking
- Scope (local / global)
- Docstrings and type hints
- Practical patterns for data processing

본 파일은 파이썬 함수의 심화 개념을 다룹니다.
실제 데이터 분석, 연구 코드, 서비스 코드에서
함수를 어떻게 "안전하고 확장 가능하게" 작성하는지가 핵심입니다.
"""

from __future__ import annotations


# ---------------------------------------------------------
# 1. Default Arguments (기본값 인자)
# ---------------------------------------------------------
# 함수 인자에 기본값을 지정할 수 있습니다.
# 실무에서는 "옵션 파라미터"를 표현할 때 매우 자주 사용됩니다.

def greet(name: str, greeting: str = "Hello") -> str:
    """
    Return a greeting message.

    Parameters
    ----------
    name : str
        Name of the person
    greeting : str, optional
        Greeting message (default: "Hello")

    Returns
    -------
    str
        Formatted greeting message
    """
    return f"{greeting}, {name}!"


print(greet("Junyeong"))
print(greet("Junyeong", "Hi"))


# ---------------------------------------------------------
# 2. *args (가변 위치 인자)
# ---------------------------------------------------------
# *args는 여러 개의 위치 인자를 "튜플"로 받습니다.
# 입력 개수가 가변적인 경우에 유용합니다.

def sum_all(*args: int) -> int:
    """
    Sum all given numbers.

    *args는 내부적으로 tuple로 처리됩니다.
    """
    total = 0
    for n in args:
        total += n
    return total


print(sum_all(1, 2, 3))
print(sum_all(1, 2, 3, 4, 5))


# ---------------------------------------------------------
# 3. **kwargs (가변 키워드 인자)
# ---------------------------------------------------------
# **kwargs는 여러 개의 키워드 인자를 "dict"로 받습니다.
# 설정(config), 메타데이터 전달에 자주 사용됩니다.

def print_profile(**kwargs) -> None:
    """
    Print user profile information.
    """
    for key, value in kwargs.items():
        print(f"{key}: {value}")


print_profile(name="Junyeong", role="Researcher", field="ML")


# ---------------------------------------------------------
# 4. Argument Unpacking (인자 언패킹)
# ---------------------------------------------------------
# 리스트/튜플/딕셔너리를 함수 인자로 풀어서 전달할 수 있습니다.

numbers = [1, 2, 3]
print(sum_all(*numbers))  # *를 사용해 언패킹

profile = {"name": "Junyeong", "role": "Founder"}
print_profile(**profile)  # **를 사용해 언패킹


# ---------------------------------------------------------
# 5. Scope: Local vs Global
# ---------------------------------------------------------
# 변수의 유효 범위(scope)는 버그의 주요 원인 중 하나입니다.

x = 10  # global scope

def change_local():
    x = 20  # local scope
    return x

def change_global():
    global x
    x = 30


print("local:", change_local())
print("global before:", x)
change_global()
print("global after:", x)

# ⚠️ 실무 팁:
# global 사용은 최소화하는 것이 좋습니다.
# 대부분의 경우 함수 인자/반환값으로 해결 가능합니다.


# ---------------------------------------------------------
# 6. Functions as First-Class Objects
# ---------------------------------------------------------
# 파이썬에서 함수는 "객체"입니다.
# 변수에 할당하거나, 인자로 전달할 수 있습니다.

def square(n: int) -> int:
    return n * n

def apply_function(func, values):
    """
    Apply a function to a list of values.
    """
    return [func(v) for v in values]


nums = [1, 2, 3, 4]
print(apply_function(square, nums))


# ---------------------------------------------------------
# 7. Practical Pattern: Data Processing Function
# ---------------------------------------------------------
# 실무/연구에서 자주 쓰는 형태:
# - 입력 검증
# - 변환
# - 명확한 반환

def normalize_scores(scores: list[float]) -> list[float]:
    """
    Normalize scores to 0-1 range.

    Parameters
    ----------
    scores : list[float]
        Raw numeric scores

    Returns
    -------
    list[float]
        Normalized scores
    """
    if not scores:
        return []

    min_score = min(scores)
    max_score = max(scores)

    if min_score == max_score:
        return [0.0 for _ in scores]

    return [(s - min_score) / (max_score - min_score) for s in scores]


raw_scores = [70, 80, 90]
print(normalize_scores(raw_scores))


# ---------------------------------------------------------
# 8. Summary
# ---------------------------------------------------------
"""
Day 요약 (한국어)

- 기본값 인자는 함수의 유연성을 높여준다
- *args / **kwargs는 가변 입력 처리의 핵심 도구
- 함수 인자 언패킹은 코드 재사용성을 크게 높인다
- 함수 스코프를 명확히 이해하면 디버깅이 쉬워진다
- 함수는 객체이며, 다른 함수에 전달될 수 있다
- 실무 함수는 "입력 검증 + 명확한 반환"이 핵심
"""