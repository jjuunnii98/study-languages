"""
Day 5: Python String Methods (문자열 처리 / 텍스트 전처리)

이 파일에서는 데이터 분석과 개발에서 자주 쓰는 문자열 처리 패턴을 다룬다.
- 공백/대소문자 정리 (strip, lower, upper, title)
- 분리/결합 (split, join)
- 치환/검색 (replace, find, in, startswith, endswith)
- 포맷팅 (f-string)
- 실전: 입력 텍스트 정규화(normalize) 함수 만들기
"""

# ==================================================
# 1. 기본 문자열 메서드: strip / lower / upper / title
# ==================================================
raw = "   Junyeong Kim   \n"
print("raw:", repr(raw))

clean = raw.strip()  # 앞뒤 공백/개행 제거
print("strip:", repr(clean))

print("lower:", clean.lower())
print("upper:", clean.upper())
print("title:", clean.title())


# ==================================================
# 2. split / join: 텍스트를 토큰화하고 다시 결합하기
# ==================================================
sentence = "Python, SQL, JavaScript"
parts = sentence.split(",")  # 쉼표 기준 분리
print("split:", parts)

parts = [p.strip() for p in parts]  # 토큰별 공백 제거 (전처리 핵심)
print("trimmed parts:", parts)

joined = " | ".join(parts)
print("join:", joined)


# ==================================================
# 3. replace / find / in: 치환과 검색
# ==================================================
text = "I love python. python is powerful."
print("original:", text)

# replace는 '새 문자열'을 만든다 (원본은 변하지 않음)
text2 = text.replace("python", "Python")
print("replace:", text2)

# find: 첫 등장 위치, 없으면 -1
idx = text.find("python")
print("find('python'):", idx)

# in: 포함 여부 (가장 자주 씀)
print("'powerful' in text:", "powerful" in text)


# ==================================================
# 4. startswith / endswith: 패턴 검사
# ==================================================
filename = "report_2025-12-29.csv"
print("is csv?:", filename.endswith(".csv"))
print("is report?:", filename.startswith("report_"))


# ==================================================
# 5. f-string: 문자열 포맷팅 (현업/분석에서 표준)
# ==================================================
name = "Junyeong"
score = 93.4567

print(f"{name}님의 점수는 {score:.2f}점입니다.")  # 소수 2자리까지


# ==================================================
# 6. 실전: 입력 텍스트 정규화(normalize) 함수
# ==================================================
# 데이터 분석에서 가장 흔한 문제:
# - 공백이 제멋대로 들어감
# - 대소문자 혼재
# - 구분자(, / ;) 혼재
# - 불필요한 특수문자 존재

def normalize_text(s: str) -> str:
    """
    텍스트를 비교/분석하기 쉽게 정규화한다.
    규칙:
    1) 앞뒤 공백 제거
    2) 중복 공백을 1칸으로 축소
    3) 모두 소문자로 변환
    """
    s = s.strip()
    # split()은 공백 여러 개를 자동으로 분리해주므로
    # " ".join(s.split()) 형태로 중복 공백을 제거할 수 있다.
    s = " ".join(s.split())
    s = s.lower()
    return s

samples = [
    "  Hello   World  ",
    "HELLO world",
    "hello     WORLD   ",
]

for s in samples:
    print("raw -> normalized:", repr(s), "->", repr(normalize_text(s)))


# ==================================================
# 7. 실전: CSV처럼 생긴 한 줄 파싱하기
# ==================================================
# 예: "id=101, name=Junyeong, city=Seoul"
line = "id=101, name=Junyeong, city=Seoul"

pairs = [p.strip() for p in line.split(",")]
print("pairs:", pairs)

data = {}
for p in pairs:
    key, value = [x.strip() for x in p.split("=", 1)]
    data[key] = value

print("parsed dict:", data)


# ==================================================
# 8. 실전: 숫자 변환 안전 처리 (문자열 -> int/float)
# ==================================================
# 데이터에는 종종 "N/A", "", "-", "unknown" 같은 값이 섞여 있다.

def safe_int(s: str, default=None):
    s = s.strip()
    if s == "" or s.lower() in {"n/a", "na", "null", "none", "-"}:
        return default
    try:
        return int(s)
    except ValueError:
        return default

values = [" 10 ", "N/A", "", "003", "abc", "-"]
converted = [safe_int(v, default=-1) for v in values]
print("safe_int:", list(zip(values, converted)))


"""
Day 5 요약
- strip/lower/split/join/replace는 텍스트 전처리의 핵심 도구
- normalize_text 같은 '정규화 함수'를 만들면 재사용성이 크게 올라간다
- safe_int 같은 방어적 변환이 실무 데이터 품질 문제를 해결해준다
"""