"""
Day 60 — Feature Engineering: Date/Time Features (03_date_features.py)

목표
- 날짜/시간 컬럼에서 실무적으로 자주 쓰는 파생 피처를 생성한다.
- 모델 입력에 유용한 형태(수치형/범주형/주기형)로 변환한다.
- 데이터 누수(leakage)를 피하기 위한 날짜 피처 설계 원칙을 포함한다.
- "학습/추론 일관성"을 위해 재사용 가능한 유틸 함수를 제공한다.

핵심 개념(한국어)
1) Calendar features
   - year, month, day, dayofweek, is_weekend, quarter
2) Cyclical encoding (주기형 인코딩)
   - dayofweek, month, hour 등을 sin/cos로 변환 (원형 거리 보존)
3) Time delta features
   - reference_date 대비 경과일(days_since_ref)
   - 이벤트 간 간격(days_since_prev_event)
4) Business time features
   - business day 여부
   - 주말/공휴일(옵션) 처리 포인트(여기선 기본만)
5) Leakage-safe rules
   - "미래 정보"로 피처를 만들지 않는다.
   - 예: label 시점 이후의 이벤트를 사용해 피처 생성하면 누수
   - reference_date는 반드시 관측 가능한 시점 기준으로 고정해야 함

실행
- 외부 데이터 없이도 동작하도록 샘플 데이터를 생성한다.
- 결과는 DataFrame 일부와 요약 통계를 출력한다.

요구사항
- pandas, numpy
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# -------------------------------
# 0) 샘플 데이터 생성 (실행 가능)
# -------------------------------
def make_sample_event_data(n_users: int = 50, events_per_user: int = 8, random_state: int = 42) -> pd.DataFrame:
    """
    사용자별 이벤트 로그 샘플 데이터를 만든다.
    - user_id
    - event_time (datetime)
    - event_type
    - amount (예: 구매 금액)
    """
    rng = np.random.default_rng(random_state)

    user_ids = np.arange(1, n_users + 1)
    event_types = np.array(["visit", "click", "add_to_cart", "purchase"])

    rows = []
    start = pd.Timestamp("2026-01-01 08:00:00")
    end = pd.Timestamp("2026-03-01 23:00:00")
    total_seconds = int((end - start).total_seconds())

    for uid in user_ids:
        # 사용자별 이벤트 시간을 랜덤 생성 후 정렬
        offsets = rng.integers(0, total_seconds, size=events_per_user)
        times = (start + pd.to_timedelta(offsets, unit="s")).sort_values()

        for t in times:
            et = rng.choice(event_types, p=[0.45, 0.35, 0.15, 0.05])
            amount = 0.0
            if et == "purchase":
                # 구매는 금액이 발생(스케일 차이를 약간 주기)
                amount = float(rng.lognormal(mean=4.0, sigma=0.6))
            rows.append((uid, t, et, amount))

    df = pd.DataFrame(rows, columns=["user_id", "event_time", "event_type", "amount"])
    df = df.sort_values(["user_id", "event_time"]).reset_index(drop=True)
    return df


# ---------------------------------------------------------
# 1) 캘린더 피처 생성 (year/month/dow 등)
# ---------------------------------------------------------
def add_calendar_features(df: pd.DataFrame, dt_col: str, prefix: str = "dt_") -> pd.DataFrame:
    """
    날짜/시간 컬럼에서 캘린더 기반 파생 피처를 만든다.
    - 연/월/일/요일/주차/분기/주말 여부
    - 시간까지 포함 시 hour/minute도 생성

    한국어 주의:
    - 시간대(timezone)가 중요한 데이터라면, 먼저 tz를 명확히 정리(UTC 통일 등) 후 파생해야 한다.
    """
    out = df.copy()
    dt = pd.to_datetime(out[dt_col], errors="coerce")

    out[f"{prefix}year"] = dt.dt.year
    out[f"{prefix}quarter"] = dt.dt.quarter
    out[f"{prefix}month"] = dt.dt.month
    out[f"{prefix}day"] = dt.dt.day

    # Monday=0 ... Sunday=6
    out[f"{prefix}dayofweek"] = dt.dt.dayofweek
    out[f"{prefix}is_weekend"] = out[f"{prefix}dayofweek"].isin([5, 6]).astype(int)

    # ISO week (주의: pandas 버전에 따라 반환 타입 차이 가능)
    iso = dt.dt.isocalendar()
    out[f"{prefix}iso_week"] = iso.week.astype(int)
    out[f"{prefix}iso_year"] = iso.year.astype(int)

    # 시간 파트
    out[f"{prefix}hour"] = dt.dt.hour
    out[f"{prefix}minute"] = dt.dt.minute

    return out


# ---------------------------------------------------------
# 2) 주기형(cyclical) 인코딩 (sin/cos)
# ---------------------------------------------------------
def add_cyclical_encoding(df: pd.DataFrame, col: str, period: int, prefix: Optional[str] = None) -> pd.DataFrame:
    """
    주기형 변수(요일, 월, 시간)를 sin/cos로 인코딩한다.
    - 선형 인코딩의 문제(예: Sunday=6, Monday=0이 멀게 보임)를 해결한다.

    예:
    - dayofweek period=7
    - month period=12
    - hour period=24
    """
    out = df.copy()
    x = pd.to_numeric(out[col], errors="coerce").fillna(0.0).astype(float)

    pfx = prefix or col
    out[f"{pfx}_sin"] = np.sin(2 * np.pi * x / period)
    out[f"{pfx}_cos"] = np.cos(2 * np.pi * x / period)
    return out


# ---------------------------------------------------------
# 3) 레퍼런스 날짜 대비 경과일(days since ref)
# ---------------------------------------------------------
def add_days_since_reference(
    df: pd.DataFrame,
    dt_col: str,
    reference_dt: pd.Timestamp,
    new_col: str = "days_since_ref",
) -> pd.DataFrame:
    """
    특정 기준(reference_dt) 대비 경과일(혹은 경과시간)을 피처로 만든다.

    한국어 실무 포인트(누수 방지):
    - reference_dt는 "관측 가능 시점" 기준이어야 한다.
      예: 예측 시점이 2026-02-10이라면 그 이후 날짜 정보를 reference로 쓰면 누수 가능.
    """
    out = df.copy()
    dt = pd.to_datetime(out[dt_col], errors="coerce")
    delta = (dt - reference_dt).dt.total_seconds() / (60 * 60 * 24)
    out[new_col] = delta
    return out


# ---------------------------------------------------------
# 4) 사용자별 직전 이벤트 대비 경과일
# ---------------------------------------------------------
def add_days_since_previous_event(
    df: pd.DataFrame,
    user_col: str,
    dt_col: str,
    new_col: str = "days_since_prev_event",
) -> pd.DataFrame:
    """
    사용자별 이벤트 로그에서 직전 이벤트 대비 경과일을 만든다.
    - user별로 dt_col 정렬이 되어있다는 가정(아니면 정렬 먼저)

    한국어 실무 포인트:
    - 이런 피처는 "시계열/이벤트 예측"에 매우 유용하다.
    - 단, 집계/예측 시점에 따라 포함 가능한 이벤트만 사용해야 누수를 피할 수 있다.
    """
    out = df.copy()
    out[dt_col] = pd.to_datetime(out[dt_col], errors="coerce")

    out = out.sort_values([user_col, dt_col]).reset_index(drop=True)
    prev_dt = out.groupby(user_col)[dt_col].shift(1)
    delta_days = (out[dt_col] - prev_dt).dt.total_seconds() / (60 * 60 * 24)
    out[new_col] = delta_days.fillna(0.0)
    return out


# ---------------------------------------------------------
# 5) 간단 리포트 유틸
# ---------------------------------------------------------
def report_date_features(df: pd.DataFrame, cols: List[str], title: str) -> None:
    """
    생성된 날짜 피처의 분포/결측을 빠르게 확인한다.
    """
    print(f"\n=== {title} ===")
    view = df[cols].copy()
    missing = view.isna().mean().sort_values(ascending=False)
    print("\n[Missing Rate]")
    print(missing.head(10).round(4))

    numeric_cols = [c for c in cols if pd.api.types.is_numeric_dtype(view[c])]
    if numeric_cols:
        print("\n[Describe]")
        print(view[numeric_cols].describe().T.round(4).head(15))


# ---------------------------------------------------------
# 6) 메인 데모
# ---------------------------------------------------------
def main() -> None:
    df = make_sample_event_data(n_users=30, events_per_user=10, random_state=7)

    # 1) 캘린더 피처
    df1 = add_calendar_features(df, dt_col="event_time", prefix="dt_")

    # 2) 주기형 인코딩
    # 요일(0~6, period=7), 월(1~12 -> period=12), 시간(0~23 -> period=24)
    df2 = add_cyclical_encoding(df1, col="dt_dayofweek", period=7, prefix="dow")
    df2 = add_cyclical_encoding(df2, col="dt_month", period=12, prefix="month")
    df2 = add_cyclical_encoding(df2, col="dt_hour", period=24, prefix="hour")

    # 3) reference_date 대비 경과일
    # 누수 방지 관점에서 reference는 "예측/관측 기준 시점"으로 고정해야 함.
    # 여기서는 데모로 데이터 시작일을 기준으로 둔다.
    reference_dt = pd.Timestamp("2026-01-01 00:00:00")
    df3 = add_days_since_reference(df2, dt_col="event_time", reference_dt=reference_dt, new_col="days_since_2026_01_01")

    # 4) 직전 이벤트 대비 경과일
    df4 = add_days_since_previous_event(df3, user_col="user_id", dt_col="event_time", new_col="days_since_prev_event")

    # 출력/검증
    show_cols = [
        "user_id",
        "event_time",
        "event_type",
        "amount",
        "dt_year",
        "dt_month",
        "dt_dayofweek",
        "dt_is_weekend",
        "dt_hour",
        "days_since_2026_01_01",
        "days_since_prev_event",
        "dow_sin",
        "dow_cos",
        "month_sin",
        "month_cos",
        "hour_sin",
        "hour_cos",
    ]

    print("\n=== Sample rows ===")
    print(df4[show_cols].head(12).to_string(index=False))

    report_date_features(
        df4,
        cols=[
            "dt_year",
            "dt_month",
            "dt_dayofweek",
            "dt_is_weekend",
            "dt_hour",
            "days_since_2026_01_01",
            "days_since_prev_event",
            "dow_sin",
            "dow_cos",
            "month_sin",
            "month_cos",
            "hour_sin",
            "hour_cos",
        ],
        title="Date feature report (Day 60)",
    )

    print("\n✅ Done. (Day 60 date features complete)")
    print("실무 팁(한국어):")
    print("- 날짜 피처는 '예측 시점' 기준으로 생성해야 한다. (미래 이벤트를 섞으면 누수)")
    print("- 요일/시간처럼 원형(주기) 변수는 sin/cos 인코딩이 특히 유용하다.")
    print("- 사용자 이벤트 로그에서는 '직전 이벤트 간격'이 강력한 행동 피처가 된다.")


if __name__ == "__main__":
    main()