"""
Day 28: pandas GroupBy & Reshape (pivot, melt)

This module covers:
- groupby aggregation for analysis
- pivot_table for reshaping into wide format
- melt for reshaping into long (tidy) format

본 파일은 pandas의 핵심 분석 기능인 groupby 집계와
데이터 형태 변환(reshape: pivot/melt)을 다룬다.

실무에서는 다음 흐름이 매우 흔하다:
raw data -> groupby로 요약 -> pivot/melt로 리포트 형태로 변환 -> 시각화/모델링
"""

import pandas as pd


# --------------------------------------------------
# 1. Sample Dataset (Transaction-like data)
# --------------------------------------------------
# 실무에서 자주 보는 "거래/로그" 형태 데이터를 가정한다.
data = [
    {"user": "Alice", "segment": "A", "month": "2025-01", "revenue": 120, "orders": 2},
    {"user": "Alice", "segment": "A", "month": "2025-02", "revenue": 80,  "orders": 1},
    {"user": "Bob",   "segment": "B", "month": "2025-01", "revenue": 200, "orders": 3},
    {"user": "Bob",   "segment": "B", "month": "2025-02", "revenue": 50,  "orders": 1},
    {"user": "Charlie","segment":"A", "month": "2025-01", "revenue": 60,  "orders": 1},
    {"user": "Charlie","segment":"A", "month": "2025-02", "revenue": 140, "orders": 2},
    {"user": "Diana", "segment": "C", "month": "2025-01", "revenue": 90,  "orders": 1},
    {"user": "Diana", "segment": "C", "month": "2025-02", "revenue": 110, "orders": 2},
]

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)


# --------------------------------------------------
# 2. GroupBy Basics (Aggregation)
# --------------------------------------------------
# groupby는 "집계 단위"를 정의하고, 요약 통계를 만들 때 사용한다.
# 예: 세그먼트별 매출 합계, 월별 주문 수, 사용자별 평균 매출 등

segment_summary = (
    df.groupby("segment")
      .agg(
          total_revenue=("revenue", "sum"),
          avg_revenue=("revenue", "mean"),
          total_orders=("orders", "sum"),
          unique_users=("user", "nunique")
      )
      .reset_index()
)

print("\n[GroupBy] Segment summary:")
print(segment_summary)

"""
[한국어 해설]
- groupby("segment") : 세그먼트 단위로 묶음
- agg() : 여러 지표를 한 번에 생성
- ("컬럼", "집계함수") 형태로 명시하면 코드가 더 명확해진다.
"""


# --------------------------------------------------
# 3. Multi-Index GroupBy (Segment x Month)
# --------------------------------------------------
# 2개 이상의 기준(차원)으로 집계하면 실무 리포팅 형태가 된다.

seg_month_summary = (
    df.groupby(["segment", "month"])
      .agg(
          revenue_sum=("revenue", "sum"),
          orders_sum=("orders", "sum"),
          user_count=("user", "nunique")
      )
      .reset_index()
)

print("\n[GroupBy] Segment x Month summary:")
print(seg_month_summary)


# --------------------------------------------------
# 4. Pivot Table (Wide Format)
# --------------------------------------------------
# pivot_table은 "행/열" 구조로 데이터를 재구성한다.
# 예: segment를 행, month를 열로 두고 revenue 합계를 테이블 형태로 만들기

pivot_revenue = pd.pivot_table(
    df,
    index="segment",
    columns="month",
    values="revenue",
    aggfunc="sum",
    fill_value=0
)

print("\n[Pivot] Revenue by segment (rows) and month (columns):")
print(pivot_revenue)

"""
[한국어 해설]
- pivot_table은 분석 리포트/대시보드 형태로 변환할 때 자주 사용
- fill_value=0 : 값이 없는 조합은 0으로 채움 (NaN 방지)
"""


# --------------------------------------------------
# 5. Reshape Back: Melt (Long/Tidy Format)
# --------------------------------------------------
# melt는 wide -> long 형태로 변환한다.
# 시각화 라이브러리(예: seaborn/plotly)나 머신러닝 feature 구성에서 유용하다.

pivot_reset = pivot_revenue.reset_index()

melted = pivot_reset.melt(
    id_vars="segment",
    var_name="month",
    value_name="revenue_sum"
)

print("\n[Melt] Wide -> Long format:")
print(melted)

"""
[한국어 해설]
- melt는 "tidy data(정돈된 데이터)" 형태로 만드는 표준 방법
- long 형태가 되면, month를 변수로 두고 쉽게 필터/시각화/모델링 가능
"""


# --------------------------------------------------
# 6. Practical Pattern: Rank within Group (GroupBy + Sort)
# --------------------------------------------------
# 실무에서 자주 쓰는 패턴:
# "월별 매출 Top user" 같은 분석

df_sorted = df.sort_values(["month", "revenue"], ascending=[True, False])
df_sorted["rank_in_month"] = df_sorted.groupby("month")["revenue"].rank(method="dense", ascending=False)

print("\n[GroupBy + Rank] Ranking users by revenue in each month:")
print(df_sorted[["month", "user", "segment", "revenue", "rank_in_month"]])

"""
[한국어 해설]
- groupby("month")로 월 단위 그룹을 만든 후 rank() 적용
- Top-N 추출, 우선순위 결정, 리포트 생성에 매우 유용
"""


# --------------------------------------------------
# 7. Summary
# --------------------------------------------------
"""
Day 28 Summary
- groupby/agg: 분석 지표를 만드는 가장 중요한 도구
- pivot_table: wide 리포트 형태(행/열 구조)로 변환
- melt: tidy/long 형태로 되돌려 분석/시각화/모델링에 활용
- groupby + rank: Top-N / 우선순위 분석 패턴

이 세트(groupby + reshape)는
EDA/리포팅/피처 엔지니어링의 핵심 기능이다.
"""