"""
Day 55 — Outlier Handling (Data Cleaning)

This script provides production-aware outlier handling patterns for analytics/ML.
It focuses on:
- Robust detection (IQR, Robust Z-score via MAD)
- Safe capping/winsorization (percentile-based)
- Optional row filtering (only when justified)
- Clear reporting for reproducibility

본 파일은 실무형 이상치(outlier) 처리 패턴을 정리합니다.
핵심은 "무조건 제거"가 아니라, 아래 순서로 안전하게 처리하는 것입니다.

1) 이상치 탐지(탐지 기준 명확화) → 2) 영향 완화(clip/cap) → 3) 필요 시 제거(drop)
그리고 항상 "리포트"를 남겨 재현 가능하게 만듭니다.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# -----------------------------
# 0) 설정(정책) 객체
# -----------------------------
@dataclass(frozen=True)
class OutlierPolicy:
    """
    Outlier 처리 정책(룰)을 한 곳에 모아두는 용도.

    - method:
        "iqr"  : 사분위(IQR) 기반 탐지
        "mad"  : Median Absolute Deviation 기반(robust z-score) 탐지
        "pct"  : 퍼센타일 기반 캡핑(탐지보다는 clip에 적합)
    - action:
        "cap"  : 클리핑(윈저라이징)으로 영향 완화 (추천)
        "drop" : 해당 행 제거 (고위험, 신중하게)
        "flag" : 플래그 컬럼만 추가(모델링/검토용)
    """
    method: str = "iqr"
    action: str = "cap"
    iqr_k: float = 1.5  # IQR rule multiplier (보통 1.5)
    mad_z: float = 3.5  # robust z-score threshold (보통 3.5)
    cap_lower_q: float = 0.01  # cap lower quantile
    cap_upper_q: float = 0.99  # cap upper quantile
    min_non_null: int = 30  # 너무 데이터가 적은 컬럼은 과격 처리 방지


# -----------------------------
# 1) 유틸: 숫자 컬럼 선택
# -----------------------------
def select_numeric_columns(df: pd.DataFrame, include: Optional[Iterable[str]] = None) -> List[str]:
    """
    숫자형 컬럼만 선택합니다.
    include가 주어지면 해당 컬럼 중 숫자형만 필터합니다.

    한국어 설명:
    - 이상치 처리는 기본적으로 numeric feature에 적용합니다.
    - 범주형은 이상치 개념이 다르므로(희귀값 등) 별도 모듈에서 다루는 것이 안전합니다.
    """
    if include is not None:
        cols = [c for c in include if c in df.columns]
        return [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


# -----------------------------
# 2) 이상치 탐지: IQR
# -----------------------------
def iqr_bounds(s: pd.Series, k: float = 1.5) -> Tuple[float, float]:
    """
    IQR 기반 하한/상한 계산.

    lower = Q1 - k*IQR
    upper = Q3 + k*IQR

    한국어 설명:
    - IQR은 분포가 비정규/왜도가 있어도 비교적 robust합니다.
    - 단, heavy-tail(꼬리가 긴 분포)에서는 outlier가 많이 잡힐 수 있으므로
      drop보다는 cap/flag가 안전합니다.
    """
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    if pd.isna(iqr) or iqr == 0:
        return (float(q1), float(q3))
    return (float(q1 - k * iqr), float(q3 + k * iqr))


def detect_outliers_iqr(s: pd.Series, k: float = 1.5) -> pd.Series:
    """IQR 기준으로 outlier 여부(True/False) 반환."""
    x = s.dropna()
    if len(x) == 0:
        return pd.Series(False, index=s.index)
    lo, hi = iqr_bounds(x, k=k)
    return (s < lo) | (s > hi)


# -----------------------------
# 3) 이상치 탐지: MAD (Robust Z-score)
# -----------------------------
def robust_zscore_mad(s: pd.Series) -> pd.Series:
    """
    MAD 기반 robust z-score 계산.

    z = 0.6745 * (x - median) / MAD

    한국어 설명:
    - 평균/표준편차 기반 z-score는 outlier에 민감합니다.
    - MAD는 median 기반이라 outlier에 강합니다.
    """
    x = s.astype("float64")
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    if mad == 0 or np.isnan(mad):
        # MAD가 0이면 분산이 거의 없다는 의미 → z-score 의미가 약함
        return pd.Series(np.zeros(len(s)), index=s.index)
    z = 0.6745 * (x - med) / mad
    return pd.Series(z, index=s.index)


def detect_outliers_mad(s: pd.Series, z_th: float = 3.5) -> pd.Series:
    """MAD 기반 robust z-score 절댓값이 임계치 초과면 outlier."""
    z = robust_zscore_mad(s)
    return z.abs() > z_th


# -----------------------------
# 4) 이상치 영향 완화: 퍼센타일 캡핑
# -----------------------------
def cap_by_percentile(s: pd.Series, lower_q: float = 0.01, upper_q: float = 0.99) -> pd.Series:
    """
    퍼센타일 기반 윈저라이징(clip).

    한국어 설명:
    - 실무에서 가장 안전한 방식 중 하나.
    - extreme 값을 잘라 모델이 outlier에 휘둘리는 것을 방지합니다.
    - 단, "정말 중요한 극단값"이 의미 있는 도메인(예: fraud)이라면
      cap 대신 별도 feature로 표시(flag)하는 전략도 고려합니다.
    """
    x = s.dropna()
    if len(x) == 0:
        return s
    lo = x.quantile(lower_q)
    hi = x.quantile(upper_q)
    return s.clip(lower=lo, upper=hi)


# -----------------------------
# 5) 메인 처리 함수: 정책 기반 적용
# -----------------------------
def apply_outlier_policy(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    policy: OutlierPolicy = OutlierPolicy(),
    flag_suffix: str = "__is_outlier",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    이상치 정책을 데이터프레임에 적용합니다.

    Returns
    -------
    cleaned_df : pd.DataFrame
        정책(action)에 따라 cap/drop/flag 적용된 결과
    report_df : pd.DataFrame
        컬럼별 이상치 개수/비율, 사용한 임계값 등 리포트

    한국어 설명:
    - 실무에서는 '무엇을 어떻게 바꿨는지' 로그/리포트가 매우 중요합니다.
    - 재현성을 위해 리포트를 DataFrame으로 반환합니다.
    """
    cleaned = df.copy()
    num_cols = select_numeric_columns(cleaned, include=columns)

    rows = []
    outlier_mask_total = pd.Series(False, index=cleaned.index)

    for col in num_cols:
        s = cleaned[col]

        non_null = s.notna().sum()
        if non_null < policy.min_non_null:
            # 데이터가 너무 적으면 공격적 outlier 처리를 피합니다.
            rows.append(
                {
                    "column": col,
                    "method": policy.method,
                    "action": "skip (too few non-null)",
                    "non_null": int(non_null),
                    "outliers": 0,
                    "outlier_rate": 0.0,
                    "notes": f"min_non_null={policy.min_non_null}",
                }
            )
            continue

        if policy.method == "iqr":
            mask = detect_outliers_iqr(s, k=policy.iqr_k)
            lo, hi = iqr_bounds(s.dropna(), k=policy.iqr_k)
            threshold_note = f"iqr_k={policy.iqr_k}, lo={lo:.6g}, hi={hi:.6g}"
        elif policy.method == "mad":
            mask = detect_outliers_mad(s, z_th=policy.mad_z)
            threshold_note = f"mad_z={policy.mad_z}"
        elif policy.method == "pct":
            # 퍼센타일 방식은 탐지보다 'cap'에 최적화
            # 그래도 참고용으로 tail(outside quantile) mask를 생성할 수 있습니다.
            x = s.dropna()
            lo = x.quantile(policy.cap_lower_q)
            hi = x.quantile(policy.cap_upper_q)
            mask = (s < lo) | (s > hi)
            threshold_note = f"cap_q=[{policy.cap_lower_q},{policy.cap_upper_q}], lo={lo:.6g}, hi={hi:.6g}"
        else:
            raise ValueError(f"Unsupported method: {policy.method}")

        outliers = int(mask.sum())
        outlier_rate = float(outliers / non_null) if non_null else 0.0

        # action 적용
        if policy.action == "flag":
            cleaned[f"{col}{flag_suffix}"] = mask.fillna(False)
        elif policy.action == "cap":
            # cap은 method에 따라 정책적으로 결정
            # - iqr/mad로 탐지하더라도 실제 처리(cap)는 퍼센타일로 하는 게 안정적일 때가 많습니다.
            cleaned[col] = cap_by_percentile(cleaned[col], policy.cap_lower_q, policy.cap_upper_q)
        elif policy.action == "drop":
            outlier_mask_total = outlier_mask_total | mask.fillna(False)
        else:
            raise ValueError(f"Unsupported action: {policy.action}")

        rows.append(
            {
                "column": col,
                "method": policy.method,
                "action": policy.action,
                "non_null": int(non_null),
                "outliers": outliers,
                "outlier_rate": round(outlier_rate, 6),
                "notes": threshold_note,
            }
        )

    if policy.action == "drop":
        before = len(cleaned)
        cleaned = cleaned.loc[~outlier_mask_total].copy()
        after = len(cleaned)
        rows.append(
            {
                "column": "__ROW_FILTER__",
                "method": policy.method,
                "action": "drop rows",
                "non_null": before,
                "outliers": int(outlier_mask_total.sum()),
                "outlier_rate": round(float(outlier_mask_total.mean()), 6),
                "notes": f"rows before={before}, after={after}",
            }
        )

    report = pd.DataFrame(rows).sort_values(by=["action", "outlier_rate"], ascending=[True, False])
    return cleaned, report


# -----------------------------
# 6) 데모 실행 (로컬 테스트)
# -----------------------------
def _demo() -> None:
    """
    데모 데이터로 동작 확인.

    한국어 설명:
    - 실제 프로젝트에서는 df를 로드한 뒤 apply_outlier_policy()를 적용합니다.
    - 여기서는 "어떤 리포트가 생성되는지" 확인하는 용도입니다.
    """
    rng = np.random.default_rng(42)
    n = 500

    df = pd.DataFrame(
        {
            "age": rng.normal(35, 10, size=n).round(0),
            "income": rng.lognormal(mean=10, sigma=0.5, size=n),
            "score": rng.normal(70, 15, size=n),
            "segment": rng.choice(["A", "B", "C"], size=n, replace=True),
        }
    )

    # 인위적으로 이상치 주입
    df.loc[rng.choice(df.index, size=5, replace=False), "income"] *= 30
    df.loc[rng.choice(df.index, size=3, replace=False), "score"] = 999

    policy = OutlierPolicy(method="iqr", action="cap", cap_lower_q=0.01, cap_upper_q=0.99)
    cleaned, report = apply_outlier_policy(df, columns=["age", "income", "score"], policy=policy)

    print("=== Outlier Report (Top) ===")
    print(report.head(10).to_string(index=False))

    # 처리 전/후 간단 비교
    print("\n=== income stats (before) ===")
    print(df["income"].describe(percentiles=[0.01, 0.5, 0.99]).to_string())
    print("\n=== income stats (after cap) ===")
    print(cleaned["income"].describe(percentiles=[0.01, 0.5, 0.99]).to_string())


if __name__ == "__main__":
    _demo()