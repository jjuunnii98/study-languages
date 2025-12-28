"""
Day 1: Python Variables

이 파일에서는 파이썬의 가장 기본적인 개념인
'변수(variable)'와 '자료형(data type)'을 다룬다.
"""

# ---------------------------
# 1. 변수란 무엇인가?
# ---------------------------
# 변수는 값을 저장하는 이름표 같은 것이다.

x = 10          # 정수(int)
y = 3.5         # 실수(float)
name = "Junyeong"  # 문자열(str)
is_student = True  # 불리언(bool)

print(x, y, name, is_student)


# ---------------------------
# 2. 변수 이름 규칙
# ---------------------------
# - 문자, 숫자, 언더스코어(_) 사용 가능
# - 숫자로 시작하면 안 됨
# - 예약어(if, for 등)는 사용 불가

my_age = 27
my_height_cm = 175

print(my_age, my_height_cm)


# ---------------------------
# 3. 자료형(type) 확인
# ---------------------------
# type() 함수로 변수의 자료형을 확인할 수 있다.

print(type(x))          # int
print(type(y))          # float
print(type(name))       # str
print(type(is_student)) # bool


# ---------------------------
# 4. 변수 값 변경
# ---------------------------
# 파이썬은 변수의 자료형이 고정되지 않는다.

score = 100
print(score, type(score))

score = "A+"
print(score, type(score))


# ---------------------------
# 5. 간단한 활용 예제
# ---------------------------
# 변수를 이용한 계산

a = 10
b = 3

sum_value = a + b
diff_value = a - b
mul_value = a * b
div_value = a / b

print("합:", sum_value)
print("차:", diff_value)
print("곱:", mul_value)
print("나눗셈:", div_value)

# ---------------------------
# 6. 변수와 입력(input)
# ---------------------------
# input() 함수는 사용자로부터 값을 문자열(str) 형태로 입력받는다.

user_name = input("이름을 입력하세요: ")
user_age = input("나이를 입력하세요: ")

print("입력된 이름:", user_name)
print("입력된 나이:", user_age)
print("user_age의 자료형:", type(user_age))  # 항상 str


# ---------------------------
# 7. 자료형 변환 (Type Casting)
# ---------------------------
# 문자열을 숫자로 변환할 수 있다.

user_age_int = int(user_age)
next_year_age = user_age_int + 1

print("내년 나이:", next_year_age)


# ---------------------------
# 8. 여러 변수 한 번에 할당하기
# ---------------------------
# 파이썬에서는 여러 변수를 한 줄에 할당할 수 있다.

a, b, c = 1, 2, 3
print(a, b, c)


# ---------------------------
# 9. 변수 값 교환 (swap)
# ---------------------------
# 임시 변수 없이 값 교환 가능

x = 5
y = 10

print("교환 전:", x, y)
x, y = y, x
print("교환 후:", x, y)


# ---------------------------
# 10. 상수(constant) 개념
# ---------------------------
# 파이썬에는 상수 문법은 없지만, 대문자로 관례적으로 표현한다.

PI = 3.14159
GRAVITY = 9.8

print("원주율:", PI)
print("중력 가속도:", GRAVITY)


"""
Day 1 추가 요약
- input()은 항상 문자열을 반환한다
- int(), float()로 자료형 변환이 가능하다
- 파이썬은 변수 교환이 매우 간단하다
- 상수는 관례적으로 대문자로 작성한다
"""