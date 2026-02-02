"""
Day 30: pandas Time Series Basics

This module covers:
- parsing datetime with to_datetime
- extracting date/time components
- sorting and indexing by datetime
- resampling time series (daily/weekly/monthly)
- rolling window statistics (moving average)

본 파일은 pandas로 시계열(time series)을 다루는 기초를 정리한다.
실무에서는 로그, 거래 데이터, 센서 데이터, 환자 기록 등에서
시간을 기준으로 집계/정렬/변환하는 작업이 매우 빈번하다.
"""

import pandas as pd


# --------------------------------------------------
# 1. Sample Time Series Dataset
# --------------------------------------------------
# 날짜 문자열을 포함한 "이벤트/거래" 형태 데이터 예시
data = [
    {"timestamp": "2025-01-01 09:10:00", "user": "Alice", "revenue": 120},
    {"timestamp": "2025-01-01 13:25:00", "user": "Bob", "revenue": 200},
    {"timestamp": "2025-01-02 10:00:00", "user": "Alice", "revenue": 80},
    {"timestamp": "2025-01-03 18:40:00", "user": "Charlie", "revenue": 60},
    {"timestamp": "2025-01-05 08:15:00", "user": "Diana", "revenue": 90},
    {"timestamp": "2025-01-06 21:30:00", "user": "Bob", "revenue": 50},
    {"timestamp": "2025-01-08 11:05:00", "user": "Charlie", "revenue": 140},
    {"timestamp": "2025-01-10 16:20:00", "user": "Diana", "revenue": 110},
]

df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)


# --------------------------------------------------
# 2. Parse datetime (to_datetime)
# --------------------------------------------------
# 문자열 -> datetime으로 변환해야 시계열 연산(resample/rolling 등)이 가능하다.
df["timestamp"] = pd.to_datetime(df["timestamp"])

print("\nAfter to_datetime:")
print(df.dtypes)

"""
[한국어 해설]
- pd.to_datetime()는 시계열 분석의 시작점
- 문자열 상태로는 날짜 계산/집계가 매우 제한적이다.
"""


# --------------------------------------------------
# 3. Extract datetime components
# --------------------------------------------------
df["date"] = df["timestamp"].dt.date
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day"] = df["timestamp"].dt.day
df["weekday"] = df["timestamp"].dt.day_name()

print("\nExtracted datetime components:")
print(df[["timestamp", "date", "year", "month", "day", "weekday"]])

"""
[한국어 해설]
- .dt accessor는 datetime Series에만 사용 가능
- year/month/day/weekday는 리포팅/특성(feature) 생성에 자주 쓰인다.
"""


# --------------------------------------------------
# 4. Sort and set datetime index
# --------------------------------------------------
df_sorted = df.sort_values("timestamp").reset_index(drop=True)
df_ts = df_sorted.set_index("timestamp")

print("\nDatetime-indexed DataFrame (sorted):")
print(df_ts.head())

"""
[한국어 해설]
- 시계열 분석은 대부분 timestamp를 index로 세팅한 후 진행
- 정렬(sort_values) 후 set_index를 해두면 resample이 쉬워진다.
"""


# --------------------------------------------------
# 5. Resampling (time-based aggregation)
# --------------------------------------------------
# 일(day) 단위 매출 합계
daily_revenue = df_ts["revenue"].resample("D").sum()

print("\n[Resample] Daily revenue sum:")
print(daily_revenue)

# 주(week) 단위 매출 합계
weekly_revenue = df_ts["revenue"].resample("W").sum()

print("\n[Resample] Weekly revenue sum:")
print(weekly_revenue)

# 월(month) 단위 매출 합계
monthly_revenue = df_ts["revenue"].resample("M").sum()

print("\n[Resample] Monthly revenue sum:")
print(monthly_revenue)

"""
[한국어 해설]
- resample("D") : 일 단위
- resample("W") : 주 단위
- resample("M") : 월 단위 (월말 기준)
- 시계열에서 '기간별 집계'는 가장 대표적인 분석 패턴이다.
"""


# --------------------------------------------------
# 6. Rolling window statistics (moving average)
# --------------------------------------------------
# 이동 평균(3일 윈도우)
daily_revenue_ma3 = daily_revenue.rolling(window=3, min_periods=1).mean()

print("\n[Rolling] 3-day moving average of daily revenue:")
print(daily_revenue_ma3)

"""
[한국어 해설]
- rolling(window=3): 최근 3기간 기준 이동 통계
- min_periods=1: 초기 구간 NaN 방지
- 금융에서는 MA(이동평균), 헬스케어에서는 추세/변화 탐지에 활용 가능
"""


# --------------------------------------------------
# 7. Time-based filtering (date slicing)
# --------------------------------------------------
# timestamp index 기반으로 기간 필터링 가능
slice_df = df_ts.loc["2025-01-01":"2025-01-05"]

print("\n[Slice] 2025-01-01 to 2025-01-05:")
print(slice_df)

"""
[한국어 해설]
- datetime index가 있으면 .loc["YYYY-MM-DD":"YYYY-MM-DD"] 형태로 범위 선택이 가능
- 실무 EDA에서 원하는 기간만 자르기(slice)는 매우 자주 발생한다.
"""


# --------------------------------------------------
# 8. Summary
# --------------------------------------------------
"""
Day 30 Summary
- to_datetime으로 문자열 날짜를 datetime으로 변환
- .dt로 날짜 구성요소 추출 (year/month/weekday 등)
- timestamp index 세팅 후 resample로 기간별 집계
- rolling으로 이동 통계 (이동평균 등) 계산
- datetime slicing으로 기간 필터링

시계열 기본기는 로그/거래/환자기록 등 거의 모든 도메인 분석에 필수다.
"""