"""
Day 41 — Regular Expressions Basics (Text Processing)

This module introduces Python's `re` library for pattern-based text matching.
Regular expressions (regex) are essential for:

- Text cleaning
- Pattern extraction
- Log parsing
- Feature engineering in NLP pipelines

이 파일은 Python의 `re` 모듈을 활용한 정규표현식 기초를 다룹니다.

정규표현식은 다음과 같은 실전 작업에서 매우 중요합니다:

- 텍스트 전처리
- 패턴 기반 정보 추출
- 로그 데이터 분석
- NLP feature engineering
"""

import re

# --------------------------------------
# 1️⃣ Basic Pattern Matching
# --------------------------------------

text = "My email is junyeong@example.com and I live in Seoul."

# Find all words starting with capital letter
pattern_capital = r"\b[A-Z][a-z]+"
capital_words = re.findall(pattern_capital, text)

print("Capitalized words:", capital_words)

"""
정규표현식 설명:
\b      : 단어 경계
[A-Z]   : 대문자 한 글자
[a-z]+  : 소문자 1개 이상
"""

# --------------------------------------
# 2️⃣ Email Extraction
# --------------------------------------

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+"
emails = re.findall(email_pattern, text)

print("Extracted emails:", emails)

"""
이메일 패턴 설명:

[a-zA-Z0-9._%+-]+   : 아이디 부분
@                   : @ 기호
[a-zA-Z0-9.-]+      : 도메인
\.                  : 점 (escape 필요)
[a-zA-Z]+           : 최상위 도메인
"""

# --------------------------------------
# 3️⃣ Substitution (Text Cleaning)
# --------------------------------------

dirty_text = "Price: $100, Discount: 20%"

cleaned_text = re.sub(r"[^0-9]", "", dirty_text)

print("Numbers only:", cleaned_text)

"""
[^0-9] : 숫자가 아닌 모든 문자
re.sub : 패턴을 다른 값으로 치환
"""

# --------------------------------------
# 4️⃣ Search vs Match
# --------------------------------------

sample = "RiskAI_2026"

print("Match result:", re.match(r"[A-Za-z]+", sample))
print("Search result:", re.search(r"\d+", sample))

"""
re.match  : 문자열 시작부터 검사
re.search : 전체 문자열에서 첫 매칭 찾기
"""

# --------------------------------------
# 5️⃣ Compiled Pattern (Performance)
# --------------------------------------

compiled_pattern = re.compile(r"\d+")

numbers = compiled_pattern.findall("Order 123, Invoice 456, Ref 789")

print("Numbers extracted:", numbers)

"""
re.compile을 사용하면 반복 패턴 검색 시 성능 향상
대량 텍스트 처리에서 중요
"""

# --------------------------------------
# 6️⃣ Practical Mini Example: Text Normalization
# --------------------------------------

raw_text = "UserID: #1234 | Status: ACTIVE | Date: 2026-01-01"

user_id = re.search(r"#(\d+)", raw_text)
date = re.search(r"\d{4}-\d{2}-\d{2}", raw_text)

if user_id:
    print("User ID:", user_id.group(1))

if date:
    print("Date:", date.group())

"""
(\d+) : 그룹 캡처
group(1) : 첫 번째 캡처 그룹 반환

정규표현식은 단순 검색이 아니라
구조화된 정보 추출 도구이다.
"""

# --------------------------------------
# 7️⃣ Summary
# --------------------------------------

"""
Regex 핵심 개념 요약:

- Pattern = 문자열 규칙 정의
- re.findall() → 모든 매칭 반환
- re.search() → 첫 매칭 반환
- re.match() → 시작 위치에서만 검사
- re.sub() → 치환
- re.compile() → 반복 작업 최적화

텍스트 데이터 전처리의 핵심 도구
"""