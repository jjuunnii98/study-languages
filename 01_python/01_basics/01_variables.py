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


"""
Day 1 요약
- 변수는 값을 저장하는 이름이다
- 파이썬은 동적 타이핑 언어다
- type()으로 자료형을 확인할 수 있다
"""