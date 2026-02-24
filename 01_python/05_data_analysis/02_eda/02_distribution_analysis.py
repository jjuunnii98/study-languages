"""
Day 51: Distribution Analysis (EDA)

목표:
- 수치형 변수의 분포 특성을 정량적으로 진단한다.
- 왜도(skewness), 첨도(kurtosis), 분위수(quantiles)를 통해
  변환(log, sqrt, Box-Cox/Yeo-Johnson 등) 후보를 판단한다.
- 히스토그램/박스플롯/QQ-plot로 정규성/이상치 영향을 시각적으로 확인한다.

주의:
- 본 파일은 "데이터셋을 읽고 바로 실행 가능한 구조"를 제공한다.
- 데이터 경로는 상황에 맞게 바꾸거나, 상위 모듈에서 DataFrame을 주입해도 된다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, Optional, Tuple, Dict, Any, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# stats는 scipy가 있으면 더 좋지만, 기본 환경에 없을 수 있으니 안전하게 처리
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except Exception:
    SCIPY_AVAILABLE = False


# ---------------------------
# 0) 설정값(필요 시 수정)
# ---------------------------
DEFAULT_NUMERIC_QUANTILES = (0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99)
DEFAULT_MAX_PLOTS = 6  # 한 번에 너무 많은 플롯을 만들지 않도록 제한


@dataclass
class DistributionSummary:
    """한 컬럼의 분포 진단 결과를 담는 데이터 클래스."""
    feature: str
    n: int
    n_missing: int
    mean: float
    std: float
    min: float
    q01: float
    q05: float
    q25: float
    q50: float
    q75: float
    q95: float
    q99: float
    max: float
    skew: float
    kurtosis: float
    iqr: float
    outlier_count_iqr: int
    outlier_rate_iqr: float
    transform_hint: str


# ---------------------------
# 1) 유틸 함수들
# ---------------------------
def detect_numeric_columns(df: pd.DataFrame) -> List[str]:
    """수치형 컬럼 목록을 반환."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def safe_skew_kurtosis(x: pd.Series) -> Tuple[float, float]:
    """
    왜도/첨도를 계산.
    - scipy가 있으면 stats.skew/kurtosis로 계산 (편향 보정 포함 옵션 가능)
    - 없으면 pandas의 Series.skew/kurt로 계산
    """
    x_clean = x.dropna()
    if len(x_clean) < 3:
        return (np.nan, np.nan)

    if SCIPY_AVAILABLE:
        skew = float(stats.skew(x_clean, bias=False))
        kurt = float(stats.kurtosis(x_clean, fisher=True, bias=False))  # fisher=True => 정규분포 첨도 0 기준
        return skew, kurt

    return float(x_clean.skew()), float(x_clean.kurt())


def iqr_outlier_count(x: pd.Series) -> Tuple[int, float, float]:
    """
    IQR(사분위 범위) 기반 이상치 개수 계산.
    - 하한: Q1 - 1.5*IQR
    - 상한: Q3 + 1.5*IQR
    """
    x_clean = x.dropna()
    if len(x_clean) == 0:
        return 0, np.nan, np.nan

    q1 = x_clean.quantile(0.25)
    q3 = x_clean.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        return 0, float(iqr), float(iqr)

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = ((x_clean < lower) | (x_clean > upper)).sum()
    return int(outliers), float(iqr), float(outliers / len(x_clean))


def transform_recommendation(skew: float) -> str:
    """
    왜도 기반으로 변환 힌트 제공 (정답이 아니라 후보를 제안하는 용도).
    - skew > 1: 강한 양의 왜도(오른쪽 꼬리) → log / sqrt 후보
    - skew < -1: 강한 음의 왜도(왼쪽 꼬리) → 제곱/반사/Box-Cox/YJ 후보
    """
    if np.isnan(skew):
        return "insufficient_data"

    if skew > 1.0:
        return "right_skewed → consider log1p / sqrt / Yeo-Johnson"
    if skew > 0.5:
        return "moderate_right_skew → consider log1p / sqrt"
    if skew < -1.0:
        return "left_skewed → consider power transform / reflect+log / Yeo-Johnson"
    if skew < -0.5:
        return "moderate_left_skew → consider power transform / Yeo-Johnson"
    return "approximately_symmetric"


def summarize_distribution(
    df: pd.DataFrame,
    numeric_cols: Optional[Iterable[str]] = None,
    quantiles: Tuple[float, ...] = DEFAULT_NUMERIC_QUANTILES,
) -> pd.DataFrame:
    """
    수치형 컬럼들에 대해 분포 진단 요약 테이블 생성.
    - 평균/표준편차/분위수
    - 왜도/첨도
    - IQR 이상치 비율
    """
    if numeric_cols is None:
        numeric_cols = detect_numeric_columns(df)

    results: List[DistributionSummary] = []

    for col in numeric_cols:
        s = df[col]
        n = int(s.shape[0])
        n_missing = int(s.isna().sum())
        s_clean = s.dropna()

        if len(s_clean) == 0:
            # 전부 결측치인 경우
            results.append(
                DistributionSummary(
                    feature=col, n=n, n_missing=n_missing,
                    mean=np.nan, std=np.nan, min=np.nan,
                    q01=np.nan, q05=np.nan, q25=np.nan, q50=np.nan, q75=np.nan, q95=np.nan, q99=np.nan,
                    max=np.nan, skew=np.nan, kurtosis=np.nan, iqr=np.nan,
                    outlier_count_iqr=0, outlier_rate_iqr=np.nan,
                    transform_hint="all_missing"
                )
            )
            continue

        qs = s_clean.quantile(list(quantiles)).to_dict()
        # 안전하게 필요한 분위수만 가져오기
        q01 = float(qs.get(0.01, np.nan))
        q05 = float(qs.get(0.05, np.nan))
        q25 = float(qs.get(0.25, np.nan))
        q50 = float(qs.get(0.50, np.nan))
        q75 = float(qs.get(0.75, np.nan))
        q95 = float(qs.get(0.95, np.nan))
        q99 = float(qs.get(0.99, np.nan))

        skew, kurt = safe_skew_kurtosis(s_clean)
        out_cnt, iqr, out_rate = iqr_outlier_count(s_clean)

        results.append(
            DistributionSummary(
                feature=col,
                n=n,
                n_missing=n_missing,
                mean=float(s_clean.mean()),
                std=float(s_clean.std(ddof=1)),
                min=float(s_clean.min()),
                q01=q01, q05=q05, q25=q25, q50=q50, q75=q75, q95=q95, q99=q99,
                max=float(s_clean.max()),
                skew=float(skew),
                kurtosis=float(kurt),
                iqr=float(iqr),
                outlier_count_iqr=int(out_cnt),
                outlier_rate_iqr=float(out_rate),
                transform_hint=transform_recommendation(float(skew)),
            )
        )

    summary_df = pd.DataFrame([r.__dict__ for r in results])
    # 보기 좋게 정렬: 결측치 적고(outlier 적고) 분포 대칭인 컬럼 우선 등은 취향 영역
    return summary_df.sort_values(by=["n_missing", "outlier_rate_iqr"], ascending=[True, True])


# ---------------------------
# 2) 시각화 함수들
# ---------------------------
def plot_hist_box_qq(
    df: pd.DataFrame,
    col: str,
    bins: int = 30,
) -> None:
    """
    한 컬럼에 대해:
    - 히스토그램
    - 박스플롯
    - QQ plot(정규성 확인)
    을 출력.

    QQ plot은 scipy가 있을 때만 제공.
    """
    s = df[col].dropna()
    if len(s) == 0:
        print(f"[skip] {col}: all missing")
        return

    # 히스토그램
    plt.figure()
    plt.hist(s, bins=bins)
    plt.title(f"Histogram: {col}")
    plt.xlabel(col)
    plt.ylabel("count")
    plt.show()

    # 박스플롯
    plt.figure()
    plt.boxplot(s, vert=True)
    plt.title(f"Boxplot: {col}")
    plt.ylabel(col)
    plt.show()

    # QQ plot (정규성 확인)
    if SCIPY_AVAILABLE:
        plt.figure()
        stats.probplot(s, dist="norm", plot=plt)
        plt.title(f"QQ Plot (Normal): {col}")
        plt.show()
    else:
        print(f"[info] scipy not available → QQ plot skipped for {col}")


def plot_top_skewed_features(
    summary_df: pd.DataFrame,
    df: pd.DataFrame,
    top_k: int = 3,
    max_plots: int = DEFAULT_MAX_PLOTS,
) -> None:
    """
    왜도 절대값이 큰 컬럼을 뽑아 시각화.
    - 분포가 치우친 컬럼은 변환 후보가 되기 쉬움.
    """
    temp = summary_df.dropna(subset=["skew"]).copy()
    if temp.empty:
        print("[info] No features with valid skewness.")
        return

    temp["abs_skew"] = temp["skew"].abs()
    candidates = temp.sort_values("abs_skew", ascending=False).head(top_k)["feature"].tolist()

    # 과도한 시각화를 막기 위한 안전장치
    candidates = candidates[: max_plots]

    for col in candidates:
        print(f"\n[plot] {col} (skew={float(summary_df.loc[summary_df.feature==col, 'skew'].values[0]):.3f})")
        plot_hist_box_qq(df, col)


# ---------------------------
# 3) 실행 예시(main)
# ---------------------------
def load_example_dataset() -> pd.DataFrame:
    """
    (예시) 로컬 CSV를 읽는 기본 함수.
    실제 프로젝트에서는 Day47~49에서 만든 로딩 유틸을 재사용해도 좋다.

    ✅ 사용 방법:
    - 아래 DATA_PATH를 본인 파일로 수정
    - 또는 이 함수를 쓰지 말고, 분석할 df를 직접 만들어서 summarize_distribution(df) 실행
    """
    DATA_PATH = os.environ.get("EDA_DATA_PATH", "")  # 환경변수로도 받을 수 있게 설계
    if not DATA_PATH:
        raise FileNotFoundError(
            "EDA_DATA_PATH is not set. "
            "Set env var EDA_DATA_PATH to your CSV path, or modify DATA_PATH in code."
        )

    df = pd.read_csv(DATA_PATH)
    return df


def main():
    # 1) 데이터 불러오기
    # - 실제로는 load_example_dataset() 대신 본인 로딩 루틴을 연결하세요.
    try:
        df = load_example_dataset()
    except Exception as e:
        print("[error] dataset load failed:", e)
        print("→ 해결: EDA_DATA_PATH 환경변수를 설정하거나, DATA_PATH를 직접 수정하세요.")
        return

    # 2) 수치형 컬럼 자동 탐지
    numeric_cols = detect_numeric_columns(df)
    print(f"[info] numeric columns: {len(numeric_cols)}")

    # 3) 분포 요약 테이블 생성
    summary_df = summarize_distribution(df, numeric_cols=numeric_cols)
    print("\n[Distribution Summary - head]")
    print(summary_df.head(10).to_string(index=False))

    # 4) 왜도가 큰 컬럼 top-K 시각화 (히스토그램/박스플롯/QQ)
    # - 실무에서는 한 번에 많은 플롯은 피하고, top-k로 좁혀 보는 게 효율적
    plot_top_skewed_features(summary_df, df, top_k=3)

    # 5) 결과 저장(선택)
    # - 보고서/재현성 관점에서 summary를 저장해두면 좋음
    out_path = "distribution_summary_day51.csv"
    summary_df.to_csv(out_path, index=False)
    print(f"\n[done] saved summary to: {out_path}")


if __name__ == "__main__":
    main()