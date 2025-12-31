"""
Day (Core): Comprehensions & Lambda

This file covers:
- List/Dict/Set comprehensions (컴프리헨션)
- Lambda functions (람다)
- Key patterns used in data cleaning and feature engineering

본 파일은 파이썬다운(Pythonic) 코드 작성의 핵심 패턴인
컴프리헨션과 람다를 다룹니다.
데이터 전처리/특징 생성(Feature Engineering)에서 매우 자주 사용됩니다.
"""

from __future__ import annotations


# ---------------------------------------------------------
# 1. Comprehension Basics
# ---------------------------------------------------------
# 컴프리헨션(comprehension)은 "반복 + 조건 + 변환"을 한 줄로 표현하는 문법입니다.
# 장점:
# - 코드가 짧고 명확해짐
# - 전처리/변환 파이프라인 작성에 유리
# 주의:
# - 너무 복잡해지면 가독성이 떨어짐 (2중 이상 중첩은 특히 주의)

nums = [1, 2, 3, 4, 5]

# (1) List comprehension: 각 원소를 제곱
squares = [n**2 for n in nums]
print("squares:", squares)

# (2) Conditional filtering: 짝수만 추출
evens = [n for n in nums if n % 2 == 0]
print("evens:", evens)

# (3) Transform + filter: 짝수만 제곱
even_squares = [n**2 for n in nums if n % 2 == 0]
print("even_squares:", even_squares)


# ---------------------------------------------------------
# 2. Dict comprehension
# ---------------------------------------------------------
# 딕셔너리 컴프리헨션은 (key: value) 형태로 만듭니다.
# 예: 숫자를 key로, 제곱을 value로 매핑

square_map = {n: n**2 for n in nums}
print("square_map:", square_map)

# 조건을 넣어 특정 조건만 포함 가능
even_square_map = {n: n**2 for n in nums if n % 2 == 0}
print("even_square_map:", even_square_map)


# ---------------------------------------------------------
# 3. Set comprehension
# ---------------------------------------------------------
# set은 중복을 제거하는 자료구조입니다.
# 예: 문자열 리스트에서 길이들의 중복 제거

words = ["apple", "banana", "cherry", "apple", "date"]
length_set = {len(w) for w in words}
print("length_set:", length_set)


# ---------------------------------------------------------
# 4. Nested Comprehension (주의해서 사용)
# ---------------------------------------------------------
# 중첩 컴프리헨션은 "2중 루프"를 한 줄로 표현합니다.
# 가독성이 떨어질 수 있으므로 "짧을 때만" 권장.

matrix = [
    [1, 2, 3],
    [4, 5, 6],
]

# 2차원 리스트를 1차원으로 flatten
flat = [x for row in matrix for x in row]
print("flat:", flat)

# Tip: 복잡해지면 for-loop로 풀어쓰는 것이 더 좋습니다.
flat_verbose = []
for row in matrix:
    for x in row:
        flat_verbose.append(x)
print("flat_verbose:", flat_verbose)


# ---------------------------------------------------------
# 5. Real-world pattern: Text cleaning (전처리 예시)
# ---------------------------------------------------------
# 데이터 분석에서 흔한 케이스:
# - 공백 제거, 소문자화, 특정 문자열 제거
raw_names = ["  Junyeong ", "ALICE", " Bob  ", "", "  "]

clean_names = [n.strip().lower() for n in raw_names if n.strip() != ""]
print("clean_names:", clean_names)

# 같은 의미를 더 명확하게 표현하려면 함수를 분리하는 것도 좋습니다.


# ---------------------------------------------------------
# 6. Lambda function basics
# ---------------------------------------------------------
# lambda는 "이름 없는 짧은 함수"입니다.
# 보통 정렬(sort key), map/filter 같은 곳에서 자주 사용합니다.
# 문법: lambda <params>: <expression>
#
# 주의:
# - lambda는 한 줄 표현식만 가능
# - 복잡해지면 def로 함수 선언 권장

add = lambda a, b: a + b
print("lambda add:", add(2, 3))

# 예: (이름, 점수) 튜플 리스트를 점수 기준으로 정렬
records = [("jun", 92), ("alice", 88), ("bob", 95)]
sorted_by_score = sorted(records, key=lambda x: x[1], reverse=True)
print("sorted_by_score:", sorted_by_score)

# 예: 문자열 길이 기준 정렬
sorted_words = sorted(words, key=lambda w: len(w))
print("sorted_words:", sorted_words)


# ---------------------------------------------------------
# 7. Comprehension + Lambda (데이터 처리 결합 패턴)
# ---------------------------------------------------------
# 예: 숫자 문자열을 정수로 바꾸고, 짝수만 남긴 뒤, 제곱
raw_nums = ["1", "2", "3", "4", "5", "6"]

to_int = lambda s: int(s)  # 변환 함수
processed = [to_int(s) ** 2 for s in raw_nums if to_int(s) % 2 == 0]
print("processed:", processed)

# ⚠️ 위 코드는 to_int(s)를 조건/변환에서 두 번 호출 (비효율 가능)
# 개선: 먼저 변환 후 사용

converted = [to_int(s) for s in raw_nums]
processed_better = [n**2 for n in converted if n % 2 == 0]
print("processed_better:", processed_better)


# ---------------------------------------------------------
# 8. map / filter vs comprehension
# ---------------------------------------------------------
# 파이썬에서는 보통 comprehension을 더 선호하는 편입니다.
# (가독성과 디버깅이 쉬운 경우가 많음)

nums2 = [1, 2, 3, 4, 5]

# map: 함수 적용
mapped = list(map(lambda n: n * 10, nums2))
print("mapped:", mapped)

# filter: 조건 필터
filtered = list(filter(lambda n: n % 2 == 1, nums2))
print("filtered:", filtered)

# 동일 작업을 comprehension으로
mapped_comp = [n * 10 for n in nums2]
filtered_comp = [n for n in nums2 if n % 2 == 1]
print("mapped_comp:", mapped_comp)
print("filtered_comp:", filtered_comp)


"""
Day 요약 (한국어)

- Comprehension은 반복/조건/변환을 간결하게 표현하는 Pythonic 문법
- List/Dict/Set comprehension을 상황에 맞게 사용
- Lambda는 짧은 "익명 함수"로 정렬 key, 간단 변환에 유리
- 복잡해지면 lambda 대신 def로 함수 분리 (가독성/테스트/재사용성 향상)
- 실무 전처리에서는 "짧고 명확"한 코드를 최우선으로 유지
"""