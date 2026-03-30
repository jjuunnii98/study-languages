"""
============================================================
Day 78 — Python Type Hints: Basic Usage
File: 01_python/06_advanced/03_type_hints/01_basic_type_hints.py

목표
- Python의 기본 타입 힌트 문법을 이해한다.
- 함수의 입력/출력 타입을 명확히 정의한다.
- 코드 가독성과 유지보수성을 향상시킨다.
- 정적 타입 검사(mypy 등) 기반 코드 설계의 기초를 다진다.

핵심 개념
- Type Hint = "이 변수/함수는 어떤 타입을 다룬다"를 명시
- 런타임에는 강제되지 않지만, 개발 단계에서 강력한 안정성을 제공
============================================================
"""

from typing import List, Dict, Optional, Union


# ------------------------------------------------------------
# 1. 기본 변수 타입 힌트
# ------------------------------------------------------------
# 한국어 설명
# 변수에 타입을 명시적으로 선언할 수 있다.
name: str = "Junyeong"
age: int = 27
height: float = 175.5
is_active: bool = True

print(name, age, height, is_active)


# ------------------------------------------------------------
# 2. 함수 타입 힌트 (기본)
# ------------------------------------------------------------
# 한국어 설명
# 함수 입력과 반환 타입을 명확히 정의한다.
def add_numbers(a: int, b: int) -> int:
    return a + b


result: int = add_numbers(3, 5)
print("Sum:", result)


# ------------------------------------------------------------
# 3. List 타입 힌트
# ------------------------------------------------------------
# 한국어 설명
# 리스트 내부 타입까지 명시 가능
def calculate_average(scores: List[float]) -> float:
    return sum(scores) / len(scores)


avg_score: float = calculate_average([80.0, 90.5, 88.0])
print("Average Score:", avg_score)


# ------------------------------------------------------------
# 4. Dict 타입 힌트
# ------------------------------------------------------------
# 한국어 설명
# Dict[key_type, value_type] 형태
def get_student_info(student_id: int) -> Dict[str, Union[str, int]]:
    return {
        "name": "Alice",
        "age": 21,
        "major": "Statistics"
    }


student_info = get_student_info(1)
print("Student Info:", student_info)


# ------------------------------------------------------------
# 5. Optional 타입
# ------------------------------------------------------------
# 한국어 설명
# 값이 있을 수도 있고(None일 수도 있음)
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Admin"
    return None


user = find_user(2)
print("User:", user)


# ------------------------------------------------------------
# 6. Union 타입
# ------------------------------------------------------------
# 한국어 설명
# 여러 타입을 허용할 때 사용
def parse_value(value: Union[int, float]) -> float:
    return float(value)


parsed_value = parse_value(10)
print("Parsed Value:", parsed_value)


# ------------------------------------------------------------
# 7. 복합 예제 (실무 스타일)
# ------------------------------------------------------------
# 한국어 설명
# 실제 데이터 처리 함수 스타일
def summarize_scores(scores: List[float]) -> Dict[str, float]:
    return {
        "mean": sum(scores) / len(scores),
        "max": max(scores),
        "min": min(scores)
    }


summary = summarize_scores([70.0, 85.5, 90.0, 88.0])
print("Score Summary:", summary)


# ------------------------------------------------------------
# 8. Optional + Dict 결합
# ------------------------------------------------------------
# 한국어 설명
# None을 반환할 수도 있는 복합 구조
def get_risk_level(score: float) -> Optional[Dict[str, Union[str, float]]]:
    if score < 0:
        return None

    if score >= 80:
        return {"level": "HIGH", "score": score}
    elif score >= 50:
        return {"level": "MEDIUM", "score": score}
    else:
        return {"level": "LOW", "score": score}


risk = get_risk_level(72.5)
print("Risk:", risk)


# ------------------------------------------------------------
# 9. 타입 힌트의 장점 요약 출력
# ------------------------------------------------------------
print("----- Type Hints Summary -----")
print("✔ 코드 가독성 향상")
print("✔ IDE 자동완성 강화")
print("✔ 정적 분석 도구(mypy) 활용 가능")
print("✔ 협업 시 명확한 인터페이스 제공")
print("------------------------------")