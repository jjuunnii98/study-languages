"""
Day 27: pandas Selection & Filtering

This module covers essential techniques for selecting and filtering data
using pandas. These patterns are used in almost every real-world
data analysis workflow.

본 파일은 pandas에서 데이터를 선택(select)하고
조건에 따라 필터링(filter)하는 핵심 방법을 다룬다.
"""

import pandas as pd

# --------------------------------------------------
# 1. Sample DataFrame
# --------------------------------------------------
data = {
    "name": ["Alice", "Bob", "Charlie", "Diana", "Evan"],
    "age": [24, 27, 22, 25, 29],
    "score": [90, 85, 88, 92, 76],
    "passed": [True, True, True, True, False]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)


# --------------------------------------------------
# 2. Column Selection
# --------------------------------------------------
# 단일 컬럼 선택 (Series 반환)
scores = df["score"]
print("\nScore column:")
print(scores)

# 여러 컬럼 선택 (DataFrame 반환)
subset = df[["name", "score"]]
print("\nName & score columns:")
print(subset)


# --------------------------------------------------
# 3. Row Selection with loc / iloc
# --------------------------------------------------
# iloc: 정수 위치 기반 선택
print("\nFirst row using iloc:")
print(df.iloc[0])

print("\nRows 1 to 3 using iloc:")
print(df.iloc[1:4])

# loc: 라벨 기반 선택 + 조건
print("\nRows where score >= 90:")
print(df.loc[df["score"] >= 90])


# --------------------------------------------------
# 4. Boolean Filtering
# --------------------------------------------------
# 단일 조건
high_score = df[df["score"] >= 85]
print("\nScore >= 85:")
print(high_score)

# 다중 조건 (&, | 사용, 반드시 괄호 필요)
passed_and_high = df[(df["passed"] == True) & (df["score"] >= 90)]
print("\nPassed AND score >= 90:")
print(passed_and_high)


# --------------------------------------------------
# 5. isin / between / query
# --------------------------------------------------
# isin: 특정 값 목록 포함 여부
selected_names = df[df["name"].isin(["Alice", "Diana"])]
print("\nSelected names (Alice, Diana):")
print(selected_names)

# between: 범위 조건
age_between = df[df["age"].between(23, 27)]
print("\nAge between 23 and 27:")
print(age_between)

# query: 문자열 기반 조건 (가독성 ↑)
high_score_query = df.query("score >= 90 and passed == True")
print("\nQuery result (score >= 90 and passed):")
print(high_score_query)


# --------------------------------------------------
# 6. Sorting and Index Reset
# --------------------------------------------------
# 정렬
sorted_df = df.sort_values(by="score", ascending=False)
print("\nSorted by score (desc):")
print(sorted_df)

# 인덱스 재설정
reset_df = sorted_df.reset_index(drop=True)
print("\nReset index:")
print(reset_df)


# --------------------------------------------------
# 7. Why This Matters
# --------------------------------------------------
"""
선택과 필터링은 pandas 분석의 출발점이다.
- EDA에서 특정 그룹을 빠르게 확인
- 모델 학습용 데이터셋 생성
- 이상치, 조건 데이터 추출

loc / iloc / boolean indexing에 익숙해지면
pandas 분석 속도가 크게 향상된다.
"""