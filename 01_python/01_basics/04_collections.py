"""
Day 4: Python Collections (자료구조 기초)

이 파일에서는 파이썬의 대표 자료구조(컬렉션)를 다룬다.
- list (리스트): 순서 O, 변경 O
- tuple(튜플): 순서 O, 변경 X
- dict (딕셔너리): key-value, 빠른 조회
- set  (집합): 중복 X, 집합 연산

데이터 분석/개발에서 컬렉션은 거의 모든 코드의 기반이 된다.
"""

# ==================================================
# 1. list (리스트)
# ==================================================
# 리스트는 여러 값을 순서대로 저장하며, 값을 수정할 수 있다.

numbers = [10, 20, 30]
print("numbers:", numbers)

# 요소 접근(인덱싱) / 슬라이싱
print("첫 번째 요소:", numbers[0])
print("마지막 요소:", numbers[-1])
print("슬라이스(0~1):", numbers[0:2])

# 요소 추가 / 삭제
numbers.append(40)      # 맨 뒤에 추가
print("append:", numbers)

numbers.insert(1, 15)   # 특정 위치에 삽입
print("insert:", numbers)

numbers.remove(20)      # 값으로 삭제(첫 번째 20만 삭제)
print("remove:", numbers)

popped = numbers.pop()  # 맨 뒤 요소 제거 + 반환
print("pop:", numbers, "popped:", popped)

# 정렬
nums = [3, 1, 2, 10, 5]
print("원본 nums:", nums)
print("sorted(nums):", sorted(nums))  # 원본 유지, 정렬된 새 리스트 반환
nums.sort()                           # 원본 자체 정렬
print("nums.sort() 후:", nums)


# ==================================================
# 2. tuple (튜플)
# ==================================================
# 튜플은 리스트와 비슷하지만, 값이 변경되지 않는(불변, immutable) 자료구조다.
# 고정된 데이터(좌표, 설정값 등)에 자주 쓰인다.

point = (10, 20)
print("point:", point)
print("x:", point[0], "y:", point[1])

# 튜플 언패킹(unpacking)
x, y = point
print("unpacked:", x, y)

# ⚠️ 튜플은 변경 불가:
# point[0] = 99  # TypeError 발생


# ==================================================
# 3. dict (딕셔너리)
# ==================================================
# 딕셔너리는 key-value 형태로 데이터를 저장한다.
# 데이터 분석에서는 "컬럼명 -> 값" 또는 "카테고리 -> 빈도" 같은 형태로 자주 사용된다.

profile = {"name": "Junyeong", "age": 27, "is_student": True}
print("profile:", profile)

# 값 조회
print("name:", profile["name"])

# get(): 키가 없을 때 에러 대신 기본값 반환 가능
print("phone:", profile.get("phone", "N/A"))

# 값 추가/수정
profile["age"] = 28
profile["city"] = "Seoul"
print("updated profile:", profile)

# key / value / items 순회
for k in profile.keys():
    print("key:", k)

for v in profile.values():
    print("value:", v)

for k, v in profile.items():
    print(f"{k} -> {v}")


# ==================================================
# 4. set (집합)
# ==================================================
# set은 중복을 허용하지 않으며, 순서가 없다.
# 데이터 클렌징(중복 제거), 교집합/합집합 계산에 유용하다.

tags = {"python", "sql", "python"}  # 중복 제거됨
print("tags:", tags)

A = {1, 2, 3, 4}
B = {3, 4, 5}

print("합집합 A|B:", A | B)
print("교집합 A&B:", A & B)
print("차집합 A-B:", A - B)

# 리스트 중복 제거 예시
raw = ["A", "B", "A", "C", "B"]
unique = list(set(raw))
print("raw:", raw)
print("unique:", unique)  # set은 순서가 없으므로 순서 유지 필요하면 다른 방법 필요


# ==================================================
# 5. 실전 예제 1: 단어 빈도 카운트 (dict 활용)
# ==================================================
text = "python is fun and python is powerful"
words = text.split()

freq = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1

print("word frequency:", freq)


# ==================================================
# 6. 실전 예제 2: 성적 데이터 요약 (list + dict)
# ==================================================
scores = [95, 82, 77, 61, 45]

summary = {
    "count": len(scores),
    "mean": sum(scores) / len(scores),
    "min": min(scores),
    "max": max(scores),
}

print("scores summary:", summary)


"""
Day 4 요약
- list: 순서 O, 수정 O (데이터를 모아 처리할 때 기본)
- tuple: 순서 O, 수정 X (고정된 값 묶음)
- dict: key-value (룰/정책/매핑/빈도 계산에 핵심)
- set: 중복 제거, 집합 연산
"""