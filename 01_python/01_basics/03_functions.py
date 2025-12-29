"""
Day 3: Python Functions

이 파일에서는 파이썬 함수(function)의 기본 개념을 다룬다.
- 함수 정의/호출 (def)
- 매개변수(parameters)와 인자(arguments)
- 반환값(return)
- 기본값(default), 키워드 인자(keyword arguments)
- 가변 인자(*args, **kwargs) 기초
"""

# ==================================================
# 1. 함수란 무엇인가?
# ==================================================
# 함수는 "반복되는 코드를 묶어서" 재사용 가능하게 만든다.
# 입력(input)을 받아서 처리하고, 결과(output)를 반환할 수 있다.

def greet():
    """인사 메시지를 출력하는 가장 단순한 함수"""
    print("안녕하세요! 함수 학습을 시작합니다.")


greet()


# ==================================================
# 2. 매개변수와 인자
# ==================================================
# - 매개변수(parameter): 함수 정의 시 괄호 안에 쓰는 변수
# - 인자(argument): 함수 호출 시 전달하는 실제 값

def greet_name(name):
    """이름을 받아 인사하는 함수"""
    print(f"안녕하세요, {name}님!")


greet_name("Junyeong")


# ==================================================
# 3. return (반환값)
# ==================================================
# return은 함수 실행 결과를 '값'으로 돌려준다.
# print는 화면 출력, return은 값 반환 → 목적이 다르다.

def add(a, b):
    """두 수의 합을 반환"""
    return a + b


result = add(10, 3)
print("add(10, 3) =", result)


# ==================================================
# 4. 기본값(default argument)
# ==================================================
# 매개변수에 기본값을 설정하면, 호출 시 인자를 생략할 수 있다.

def power(base, exponent=2):
    """base의 exponent 제곱을 반환 (기본은 제곱)"""
    return base ** exponent


print("power(5) =", power(5))          # 5^2
print("power(5, 3) =", power(5, 3))    # 5^3


# ==================================================
# 5. 키워드 인자(keyword arguments)
# ==================================================
# 인자의 순서를 바꾸거나, 어떤 값이 어떤 매개변수로 들어가는지 명확히 할 때 사용

print("power(base=2, exponent=5) =", power(base=2, exponent=5))


# ==================================================
# 6. 여러 값을 반환하기 (튜플 반환)
# ==================================================
# 파이썬 함수는 여러 값을 "튜플" 형태로 반환할 수 있다.

def basic_stats(numbers):
    """
    숫자 리스트를 받아
    (합계, 평균, 최솟값, 최댓값)을 반환
    """
    total = sum(numbers)
    mean = total / len(numbers)
    min_val = min(numbers)
    max_val = max(numbers)
    return total, mean, min_val, max_val


nums = [10, 20, 30, 40]
total, mean, min_val, max_val = basic_stats(nums)
print("합계:", total)
print("평균:", mean)
print("최솟값:", min_val)
print("최댓값:", max_val)


# ==================================================
# 7. 가변 인자 *args, **kwargs (기초)
# ==================================================
# *args: 여러 개의 위치 인자를 튜플로 받음
# **kwargs: 여러 개의 키워드 인자를 딕셔너리로 받음

def sum_all(*args):
    """여러 숫자를 받아 모두 더한 값을 반환"""
    return sum(args)


print("sum_all(1,2,3) =", sum_all(1, 2, 3))
print("sum_all(5,10,15,20) =", sum_all(5, 10, 15, 20))


def print_profile(**kwargs):
    """키-값 형태의 정보를 받아 출력"""
    print("=== Profile ===")
    for k, v in kwargs.items():
        print(f"{k}: {v}")


print_profile(name="Junyeong", role="Student", interest="Data Science")


# ==================================================
# 8. 실전 예제: 점수 등급 함수
# ==================================================
# 점수를 입력받아 등급을 반환하는 함수 (실무에서 규칙/정책 함수로 많이 사용)

def grade(score):
    """
    점수에 따른 학점 등급을 반환
    90 이상: A
    80 이상: B
    70 이상: C
    60 이상: D
    그 외: F
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


test_scores = [95, 83, 77, 61, 45]
for s in test_scores:
    print(f"{s}점 → {grade(s)}")


"""
Day 3 요약
- 함수는 코드 재사용과 구조화의 핵심 도구다
- return은 값을 반환하고, print는 출력한다
- 기본값/키워드 인자를 사용하면 함수가 유연해진다
- *args, **kwargs는 확장성을 높이는 기초 문법이다
"""