"""
Day 50: EDA — Summary Statistics

이 파일에서는 EDA(Exploratory Data Analysis)의 첫 단계인
요약 통계(summary statistics)를 '실무/연구에서 바로 쓰는 방식'으로 정리한다.

핵심 목표:
- 데이터의 분포/규모/결측/이상치(outlier) 여부를 빠르게 스캔
- 수치형/범주형을 분리해서 요약
- 그룹별 통계로 세그먼트 차이를 탐색
- "재사용 가능한" 유틸 함수 형태로 정리

주의:
- 이 예시는 로컬 CSV가 있다고 가정하지만, 파일이 없으면 더미 데이터로 데모를 수행한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

import numpy as np
import pandas as pd


# ---------------------------
# 0. (선택) 데이터 로드
# ---------------------------
def load_data(path: str = "data/sample.csv") -> pd.DataFrame:
    """
    실무에서는 보통 data/ 폴더 아래에 원본/샘플 파일을 둔다.
    - Repo에는 전체 원본 데이터 대신 "샘플"만 두거나, 경로만 문서화하는 것이 일반적.

    여기서는 path가 없으면 더미 데이터로 EDA 흐름만 시연한다.
    """
    try:
        df = pd.read_csv(path)
        print(f"[OK] Loaded: {path} | shape={df.shape}")
        return df
    except FileNotFoundError:
        print(f"[WARN] File not found: {path} -> Using demo dataset")
        return make_demo_dataset(n=300, seed=42)


def make_demo_dataset(n: int = 200, seed: int = 0) -> pd.DataFrame:
    """
    데모용 데이터셋 생성.
    - 결측치/이상치/범주형을 일부 섞어서 EDA가 의미 있게 동작하도록 만든다.
    """
    rng = np.random.default_rng(seed)
    age = rng.normal(35, 12, size=n).round().astype(int)
    income = rng.lognormal(mean=10.3, sigma=0.4, size=n)  # 소득처럼 오른쪽 꼬리 분포
    score = rng.normal(70, 10, size=n)

    # 이상치 삽입(소수)
    outlier_idx = rng.choice(n, size=max(1, n // 50), replace=False)
    income[outlier_idx] *= 8

    # 결측치 삽입
    miss_idx = rng.choice(n, size=max(1, n // 25), replace=False)
    score[miss_idx] = np.nan

    city = rng.choice(["Seoul", "Busan", "Incheon", "Daegu"], size=n, p=[0.55, 0.2, 0.15, 0.1])
    segment = rng.choice(["A", "B", "C"], size=n, p=[0.5, 0.35, 0.15])

    df = pd.DataFrame(
        {
            "age": age,
            "income": income,
            "score": score,
            "city": city,
            "segment": segment,
        }
    )
    return df


# ---------------------------
# 1. 데이터 구조 점검(Shape/Types/Head)
# ---------------------------
def basic_profile(df: pd.DataFrame, n_head: int = 5) -> None:
    """
    가장 먼저 보는 3종 세트:
    1) shape (행/열)
    2) dtypes (타입)
    3) head (상단 몇 줄)

    이 단계에서:
    - 날짜가 문자열로 들어왔는지
    - 숫자 컬럼이 object로 들어왔는지
    - 의미 없는 id/상수 컬럼이 있는지
    를 빠르게 확인한다.
    """
    print("\n[1] BASIC PROFILE")
    print(f"shape = {df.shape}")
    print("\n[dtypes]")
    print(df.dtypes)
    print("\n[head]")
    print(df.head(n_head))


# ---------------------------
# 2. 결측치 요약(Missingness)
# ---------------------------
def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    결측치는 EDA에서 가장 중요한 이슈 중 하나.
    - 결측률이 높은 컬럼은 제거/대체/추가 수집 등 전략이 필요하다.

    반환값:
    - 결측 개수, 결측 비율(%)을 내림차순으로 정렬한 테이블
    """
    miss_cnt = df.isna().sum()
    miss_rate = (miss_cnt / len(df) * 100).round(2)
    out = (
        pd.DataFrame({"missing_count": miss_cnt, "missing_rate_pct": miss_rate})
        .sort_values("missing_rate_pct", ascending=False)
        .query("missing_count > 0")
    )
    return out


# ---------------------------
# 3. 수치형 요약 통계(Descriptive stats)
# ---------------------------
@dataclass(frozen=True)
class NumericSummaryConfig:
    """
    수치형 요약에서 실무적으로 자주 쓰는 설정을 묶어서 관리.
    """
    percentiles: tuple[float, ...] = (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)
    include_skew_kurt: bool = True
    iqr_outlier_factor: float = 1.5  # IQR 기반 이상치 경계


def numeric_summary(df: pd.DataFrame, config: Optional[NumericSummaryConfig] = None) -> pd.DataFrame:
    """
    수치형 컬럼에 대해:
    - count/mean/std/min/max
    - 지정 분위수(percentiles)
    - (선택) 왜도(skewness), 첨도(kurtosis)
    - (선택) IQR 기반 이상치 개수
    를 한 번에 정리한다.
    """
    if config is None:
        config = NumericSummaryConfig()

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num_cols:
        return pd.DataFrame()

    desc = df[num_cols].describe(percentiles=list(config.percentiles)).T

    # 왜도/첨도(분포의 비대칭/뾰족함)
    if config.include_skew_kurt:
        desc["skew"] = df[num_cols].skew(numeric_only=True)
        desc["kurtosis"] = df[num_cols].kurt(numeric_only=True)

    # IQR 기반 이상치 개수(빠른 스캔 용도)
    q1 = df[num_cols].quantile(0.25)
    q3 = df[num_cols].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - config.iqr_outlier_factor * iqr
    upper = q3 + config.iqr_outlier_factor * iqr

    outlier_mask = (df[num_cols] < lower) | (df[num_cols] > upper)
    desc["iqr_outlier_count"] = outlier_mask.sum(axis=0)

    # 보기 좋게 컬럼 정렬(선호에 따라 조정 가능)
    # describe 결과 컬럼명은 pandas 버전에 따라 조금 다를 수 있음
    return desc


# ---------------------------
# 4. 범주형 요약 통계(Categorical stats)
# ---------------------------
def categorical_summary(df: pd.DataFrame, top_k: int = 10) -> dict[str, pd.DataFrame]:
    """
    범주형 컬럼은:
    - 유니크 개수(cardinality)
    - 상위 빈도값(top frequency)
    - 희귀값(rare) 존재 여부
    를 보는 것이 핵심.

    반환:
    - 컬럼별 value_counts 테이블(dict)
    """
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    results: dict[str, pd.DataFrame] = {}

    for c in cat_cols:
        vc = df[c].value_counts(dropna=False).head(top_k)
        tbl = vc.to_frame(name="count")
        tbl["rate_pct"] = (tbl["count"] / len(df) * 100).round(2)
        results[c] = tbl

    return results


# ---------------------------
# 5. 그룹별 요약(Grouped stats)
# ---------------------------
def grouped_numeric_summary(
    df: pd.DataFrame,
    group_col: str,
    target_cols: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """
    세그먼트/도시/성별 등 그룹에 따라 수치형의 평균/중앙값이 달라지는지 확인.
    - 실제 분석에서 feature/segment 차이를 확인하는 가장 빠른 방법 중 하나.

    기본은 df의 모든 수치형 컬럼을 대상으로 한다.
    """
    if group_col not in df.columns:
        raise ValueError(f"group_col not found: {group_col}")

    if target_cols is None:
        target_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    target_cols = [c for c in target_cols if c in df.columns]
    if not target_cols:
        return pd.DataFrame()

    agg = (
        df.groupby(group_col)[target_cols]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .round(3)
    )
    return agg


# ---------------------------
# 6. 실행 엔트리 포인트
# ---------------------------
def main() -> None:
    df = load_data("data/sample.csv")

    basic_profile(df)

    miss = missing_summary(df)
    print("\n[2] MISSING SUMMARY")
    print(miss if not miss.empty else "No missing values.")

    num_sum = numeric_summary(df)
    print("\n[3] NUMERIC SUMMARY")
    print(num_sum)

    cat_sum = categorical_summary(df, top_k=10)
    print("\n[4] CATEGORICAL SUMMARY (Top-K)")
    if not cat_sum:
        print("No categorical columns.")
    else:
        for col, table in cat_sum.items():
            print(f"\n- {col}")
            print(table)

    # 그룹 예시(존재할 때만)
    if "segment" in df.columns:
        grp = grouped_numeric_summary(df, "segment")
        print("\n[5] GROUPED NUMERIC SUMMARY by segment")
        print(grp)

    print("\n[Done] Day 50 summary statistics EDA completed.")


if __name__ == "__main__":
    main()