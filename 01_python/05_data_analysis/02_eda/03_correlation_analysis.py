"""
Day 52: Correlation Analysis (EDA)

목표
- 수치형 변수 간 상관관계를 정량적으로 분석한다.
- Pearson / Spearman 상관계수를 비교한다.
- 타깃(있다면)과의 상관 Top-K를 추출한다.
- 다중공선성(예: |corr| >= threshold) 후보 쌍을 탐지한다.
- 결과를 재사용 가능한 형태(함수)로 구성한다.

주의
- 상관관계는 인과가 아니다.
- Pearson: 선형 관계에 민감 (정규성/선형성 가정에 더 가까움)
- Spearman: 순위 기반, 단조 관계를 더 잘 잡고 이상치에 비교적 강함
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Tuple

import numpy as np
import pandas as pd


# -----------------------------
# 0. 설정값 / 결과 구조
# -----------------------------
@dataclass(frozen=True)
class CorrPair:
    """상관이 높은 변수 쌍을 표현하는 구조체"""
    var_a: str
    var_b: str
    corr: float


# -----------------------------
# 1. 유틸 함수들
# -----------------------------
def select_numeric_df(df: pd.DataFrame, drop_all_na: bool = True) -> pd.DataFrame:
    """
    수치형 컬럼만 추출한다.
    - drop_all_na: 전부 NA인 컬럼 제거 여부
    """
    numeric = df.select_dtypes(include=[np.number]).copy()
    if drop_all_na:
        numeric = numeric.dropna(axis=1, how="all")
    return numeric


def correlation_matrix(
    df_numeric: pd.DataFrame,
    method: str = "pearson",
    min_non_na: int = 3,
) -> pd.DataFrame:
    """
    상관행렬을 계산한다.
    - method: 'pearson' | 'spearman'
    - min_non_na: 상관 계산에 필요한 최소 유효 관측치(결측 제외) 기준
      (pandas corr는 pairwise complete observations를 사용)
    """
    if method not in {"pearson", "spearman"}:
        raise ValueError("method must be one of {'pearson', 'spearman'}")

    # 유효한 데이터가 너무 적은 컬럼이 있으면 상관이 불안정해지므로 필터링 가능
    valid_counts = df_numeric.notna().sum(axis=0)
    filtered = df_numeric.loc[:, valid_counts >= min_non_na]

    if filtered.shape[1] < 2:
        return pd.DataFrame()

    return filtered.corr(method=method)


def top_correlations_with_target(
    df_numeric: pd.DataFrame,
    target: str,
    method: str = "pearson",
    top_k: int = 10,
    absolute: bool = True,
) -> pd.DataFrame:
    """
    타깃 컬럼과 다른 수치형 변수들의 상관 Top-K를 반환한다.
    - absolute: True면 |corr| 기준으로 정렬
    """
    if target not in df_numeric.columns:
        raise ValueError(f"target '{target}' not found in numeric columns")

    corr_series = df_numeric.corr(method=method)[target].drop(labels=[target], errors="ignore")
    corr_series = corr_series.dropna()

    if absolute:
        corr_series = corr_series.reindex(corr_series.abs().sort_values(ascending=False).index)
    else:
        corr_series = corr_series.sort_values(ascending=False)

    result = corr_series.head(top_k).reset_index()
    result.columns = ["feature", f"{method}_corr_with_{target}"]
    return result


def find_high_corr_pairs(
    corr_mat: pd.DataFrame,
    threshold: float = 0.85,
) -> List[CorrPair]:
    """
    상관행렬에서 |corr| >= threshold인 변수 쌍을 찾아낸다.
    - 상삼각(중복 제거)만 추출한다.
    """
    if corr_mat.empty:
        return []

    # 상삼각 mask
    upper = corr_mat.where(np.triu(np.ones(corr_mat.shape), k=1).astype(bool))
    pairs = []

    # stack으로 (i,j) 형태 변환 후 필터링
    stacked = upper.stack().dropna()
    for (a, b), v in stacked.items():
        if abs(v) >= threshold:
            pairs.append(CorrPair(var_a=a, var_b=b, corr=float(v)))

    # |corr| 내림차순 정렬
    pairs.sort(key=lambda x: abs(x.corr), reverse=True)
    return pairs


def pretty_print_pairs(pairs: List[CorrPair], limit: int = 20) -> None:
    """
    상관이 높은 변수쌍을 보기 좋게 출력한다.
    """
    if not pairs:
        print("No high-correlation pairs found.")
        return

    print(f"High-correlation pairs (top {min(limit, len(pairs))}):")
    for p in pairs[:limit]:
        print(f"- {p.var_a}  <->  {p.var_b} : corr = {p.corr:.4f}")


# -----------------------------
# 2. 예시 실행 (샘플 데이터)
# -----------------------------
def build_sample_df(seed: int = 42, n: int = 200) -> pd.DataFrame:
    """
    외부 데이터가 없어도 실행 가능하도록 샘플 데이터 생성.
    - 일부 변수는 강한 상관이 발생하도록 설계
    """
    rng = np.random.default_rng(seed)
    x1 = rng.normal(0, 1, n)
    x2 = x1 * 0.9 + rng.normal(0, 0.2, n)          # x1과 높은 양의 상관
    x3 = -x1 * 0.8 + rng.normal(0, 0.3, n)         # x1과 높은 음의 상관
    x4 = rng.normal(5, 2, n)                       # 독립적
    target = 2.0 * x1 + 0.5 * x4 + rng.normal(0, 1, n)

    # 결측 일부 추가(현실 데이터 시뮬레이션)
    x2[rng.choice(n, size=10, replace=False)] = np.nan
    x4[rng.choice(n, size=5, replace=False)] = np.nan

    return pd.DataFrame(
        {
            "x1": x1,
            "x2": x2,
            "x3": x3,
            "x4": x4,
            "target": target,
        }
    )


def main(target: Optional[str] = "target") -> None:
    """
    실행 엔트리 포인트.
    - 실제 프로젝트에서는 df를 로딩해서 df_numeric에 넣으면 된다.
    """
    df = build_sample_df()
    df_numeric = select_numeric_df(df)

    print("=== Basic Info ===")
    print(df_numeric.shape)
    print(df_numeric.head(), "\n")

    # (1) Pearson / Spearman 상관행렬
    pearson_corr = correlation_matrix(df_numeric, method="pearson")
    spearman_corr = correlation_matrix(df_numeric, method="spearman")

    print("=== Pearson Correlation Matrix ===")
    print(pearson_corr.round(3), "\n")

    print("=== Spearman Correlation Matrix ===")
    print(spearman_corr.round(3), "\n")

    # (2) 타깃과의 상관 Top-K (타깃이 있는 경우)
    if target and target in df_numeric.columns:
        print("=== Top correlations with target (Pearson, |corr| desc) ===")
        print(top_correlations_with_target(df_numeric, target=target, method="pearson", top_k=10), "\n")

        print("=== Top correlations with target (Spearman, |corr| desc) ===")
        print(top_correlations_with_target(df_numeric, target=target, method="spearman", top_k=10), "\n")
    else:
        print("No target column provided or target not found. Skipping target correlation.\n")

    # (3) 다중공선성 후보 탐지: |corr| >= threshold
    threshold = 0.85
    high_pairs = find_high_corr_pairs(pearson_corr, threshold=threshold)
    print(f"=== High correlation pairs (|corr| >= {threshold}) ===")
    pretty_print_pairs(high_pairs, limit=20)

    # (4) 실무 팁 (출력)
    print("\n=== Practical Notes ===")
    print("- If two features have |corr| close to 1, consider dropping one or using regularization.")
    print("- For non-linear monotonic relationships, Spearman may capture signal better than Pearson.")
    print("- Correlation does NOT imply causation; validate with domain knowledge and modeling.")


if __name__ == "__main__":
    main(target="target")