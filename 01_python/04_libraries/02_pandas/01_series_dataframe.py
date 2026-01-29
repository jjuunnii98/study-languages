"""
Day 26: pandas Series & DataFrame Basics

This module introduces the two core data structures in pandas:
Series and DataFrame.

pandas is the primary library for data manipulation and analysis
in Python, built on top of NumPy.

본 파일은 pandas의 핵심 자료구조인
Series와 DataFrame의 기본 개념과 사용법을 다룬다.
"""

import pandas as pd

# --------------------------------------------------
# 1. pandas Series
# --------------------------------------------------
# Series는 1차원 데이터 구조로,
# NumPy 배열에 index 개념이 추가된 형태이다.

scores = pd.Series([90, 85, 88, 92],
                    index=["Alice", "Bob", "Charlie", "Diana"])

print("Series example:")
print(scores)
print("\nSeries values:")
print(scores.values)
print("\nSeries index:")
print(scores.index)

# 개별 값 접근
print("\nScore of Alice:", scores["Alice"])


# --------------------------------------------------
# 2. pandas DataFrame
# --------------------------------------------------
# DataFrame은 2차원 테이블 형태의 자료구조로,
# 실제 데이터 분석에서 가장 많이 사용된다.

data = {
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "age": [24, 27, 22, 25],
    "score": [90, 85, 88, 92]
}

df = pd.DataFrame(data)

print("\nDataFrame example:")
print(df)


# --------------------------------------------------
# 3. Basic DataFrame Inspection
# --------------------------------------------------
# 데이터 구조를 빠르게 파악하는 것이 중요하다.

print("\nDataFrame shape:", df.shape)
print("\nDataFrame columns:", df.columns)
print("\nDataFrame dtypes:")
print(df.dtypes)


# --------------------------------------------------
# 4. Column and Row Selection
# --------------------------------------------------
# 열(column) 선택
print("\nScore column:")
print(df["score"])

# 여러 열 선택
print("\nName and age columns:")
print(df[["name", "age"]])

# 행(row) 선택 - loc / iloc
print("\nFirst row using iloc:")
print(df.iloc[0])

print("\nRow where name == 'Bob':")
print(df.loc[df["name"] == "Bob"])


# --------------------------------------------------
# 5. Simple Filtering
# --------------------------------------------------
# 조건 기반 데이터 필터링

high_score_df = df[df["score"] >= 90]

print("\nStudents with score >= 90:")
print(high_score_df)


# --------------------------------------------------
# 6. Adding New Columns
# --------------------------------------------------
# 새로운 열 생성 (파생 변수)

df["passed"] = df["score"] >= 85

print("\nDataFrame with new column:")
print(df)


# --------------------------------------------------
# 7. Why This Matters
# --------------------------------------------------
"""
pandas Series와 DataFrame은 다음의 기반이 된다:
- 데이터 전처리 및 정제
- EDA (탐색적 데이터 분석)
- 통계 분석 및 피처 엔지니어링
- 머신러닝 모델 입력 데이터 구성

pandas를 자유롭게 다룰 수 있으면
실제 데이터 분석 업무의 70% 이상을 커버할 수 있다.
"""