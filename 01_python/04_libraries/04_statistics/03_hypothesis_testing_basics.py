"""
Day 36: Hypothesis Testing Basics (가설검정 기초)

[EN]
This file provides a practical, code-first introduction to hypothesis testing:
- One-sample t-test (approx, normal assumption)
- Two-sample Welch's t-test (recommended default for two means)
- Chi-square test of independence for 2x2 tables (approx)
- Effect sizes (Cohen's d, Hedges' g, Cramér's V)
- Simple permutation test (distribution-free validation)

[KR]
이 파일은 가설검정을 "공식 암기"가 아니라
실무/연구에서 재현 가능한 코드 구조로 정리한다.

포인트:
1) 가설(H0/H1) 정의
2) 검정 선택 (데이터/가정 기반)
3) 통계량 계산
4) p-value 해석
5) 효과크기(effect size)까지 보고 "실질적 유의성" 판단

✅ 외부 라이브러리 없이 실행 가능
(참고: SciPy가 있으면 더 정확하고 편리하지만, 여기서는 기본 원리/구조에 집중)
"""

from __future__ import annotations

import math
import random
import statistics as stats
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple


# ------------------------------------------------------------
# 0) Helper: basic math
# ------------------------------------------------------------

def mean(x: Sequence[float]) -> float:
    return float(sum(x) / len(x))

def variance_sample(x: Sequence[float]) -> float:
    """Sample variance with ddof=1."""
    return float(stats.variance(x)) if len(x) >= 2 else 0.0

def stdev_sample(x: Sequence[float]) -> float:
    return float(stats.stdev(x)) if len(x) >= 2 else 0.0

def pooled_stdev(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Pooled standard deviation (assuming equal variances).
    [KR] 등분산 가정 하에서 Cohen's d 계산에 사용.
    """
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return 0.0
    vx = variance_sample(x)
    vy = variance_sample(y)
    pooled_var = ((nx - 1) * vx + (ny - 1) * vy) / (nx + ny - 2)
    return float(math.sqrt(pooled_var))


# ------------------------------------------------------------
# 1) Effect sizes
# ------------------------------------------------------------

def cohens_d(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Cohen's d (standardized mean difference) using pooled SD.
    [KR] 평균 차이를 표준화한 효과크기.
    """
    s = pooled_stdev(x, y)
    if s == 0:
        return 0.0
    return (mean(x) - mean(y)) / s

def hedges_g(x: Sequence[float], y: Sequence[float]) -> float:
    """
    Hedges' g: bias-corrected Cohen's d for small samples.
    [KR] 표본이 작을 때 Cohen's d의 편향을 보정한 효과크기.
    """
    d = cohens_d(x, y)
    nx, ny = len(x), len(y)
    df = nx + ny - 2
    if df <= 0:
        return d
    J = 1 - (3 / (4 * df - 1))  # correction factor
    return J * d

def cramers_v_2x2(a: int, b: int, c: int, d: int) -> float:
    """
    Cramér's V for 2x2 contingency table.
    Table:
        Col1 Col2
    Row1  a    b
    Row2  c    d

    [KR] 범주형 독립성 검정(카이제곱)에서 효과크기 지표.
    """
    n = a + b + c + d
    if n == 0:
        return 0.0
    # phi coefficient for 2x2
    denom = math.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    if denom == 0:
        return 0.0
    phi = (a * d - b * c) / denom
    return abs(phi)


# ------------------------------------------------------------
# 2) Approx p-value functions (no SciPy)
# ------------------------------------------------------------
# NOTE:
# - 정확한 t-distribution CDF 구현은 복잡하므로,
#   여기서는 "구조/해석/효과크기"에 초점을 둔다.
# - p-value는 (a) permutation test로 보완하거나,
#   (b) SciPy를 사용하면 정확해진다.
#
# 아래는 실무에서 "대략적" 참고용으로 사용할 수 있는
# 정규근사 기반 p-value 계산을 제공한다.

def normal_cdf(z: float) -> float:
    """Standard normal CDF using error function."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

def two_sided_p_from_z(z: float) -> float:
    """Two-sided p-value from z-score under standard normal approximation."""
    p_one = 1.0 - normal_cdf(abs(z))
    return 2.0 * p_one


# ------------------------------------------------------------
# 3) One-sample test (mean vs mu0) - normal approx
# ------------------------------------------------------------

@dataclass(frozen=True)
class OneSampleTestResult:
    n: int
    mean: float
    mu0: float
    t_stat: float
    p_value_approx: float
    interpretation_kr: str


def one_sample_mean_test_normal_approx(x: Sequence[float], mu0: float) -> OneSampleTestResult:
    """
    One-sample t-stat but p-value via normal approximation.

    [KR]
    1표본 평균 검정 구조:
    - H0: mu = mu0
    - H1: mu != mu0
    t = (xbar - mu0) / (s / sqrt(n))

    p-value는 표준정규근사로 계산(대략).
    정확한 p-value는 SciPy or t분포 CDF 필요.
    """
    if len(x) < 2:
        raise ValueError("Need at least 2 observations for variance.")

    n = len(x)
    xbar = mean(x)
    s = stdev_sample(x)
    se = s / math.sqrt(n)
    t = (xbar - mu0) / se if se != 0 else 0.0

    # 대략적 p-value (정규근사)
    p = two_sided_p_from_z(t)

    interp = (
        "p-value가 작으면(예: <0.05) H0를 기각할 근거가 있다. "
        "단, 이는 정규근사 기반의 대략값이므로 정확한 검정이 필요하면 SciPy 사용 권장."
    )
    return OneSampleTestResult(n=n, mean=xbar, mu0=mu0, t_stat=t, p_value_approx=p, interpretation_kr=interp)


# ------------------------------------------------------------
# 4) Two-sample Welch test (means) - normal approx
# ------------------------------------------------------------

@dataclass(frozen=True)
class TwoSampleTestResult:
    n1: int
    n2: int
    mean1: float
    mean2: float
    diff: float
    welch_t: float
    p_value_approx: float
    effect_size_g: float
    interpretation_kr: str


def welch_t_test_normal_approx(x: Sequence[float], y: Sequence[float]) -> TwoSampleTestResult:
    """
    Welch's t-test structure (unequal variances).
    p-value via normal approximation (rough).

    [KR]
    2표본 평균 차이 검정에서, 실무 기본 추천은 Welch(등분산 가정 X).
    - H0: mean(x) = mean(y)
    - H1: mean(x) != mean(y)
    """
    if len(x) < 2 or len(y) < 2:
        raise ValueError("Need at least 2 observations per group.")

    n1, n2 = len(x), len(y)
    m1, m2 = mean(x), mean(y)
    v1, v2 = variance_sample(x), variance_sample(y)

    se = math.sqrt(v1 / n1 + v2 / n2)
    t = (m1 - m2) / se if se != 0 else 0.0

    # 대략적 p-value (정규근사)
    p = two_sided_p_from_z(t)

    g = hedges_g(x, y)

    interp = (
        "Welch t-test는 분산이 달라도 평균 차이를 평가할 수 있다. "
        "p-value가 작으면 평균 차이가 통계적으로 유의할 가능성이 높다. "
        "하지만 p-value만 보지 말고 Hedges' g(효과크기)로 실질적 차이를 함께 판단하자."
    )

    return TwoSampleTestResult(
        n1=n1, n2=n2, mean1=m1, mean2=m2, diff=m1 - m2,
        welch_t=t, p_value_approx=p, effect_size_g=g, interpretation_kr=interp
    )


# ------------------------------------------------------------
# 5) Chi-square independence test (2x2) - normal approx
# ------------------------------------------------------------

@dataclass(frozen=True)
class ChiSquare2x2Result:
    chi2: float
    p_value_approx: float
    cramers_v: float
    interpretation_kr: str


def chi_square_2x2_normal_approx(a: int, b: int, c: int, d: int) -> ChiSquare2x2Result:
    """
    Compute chi-square statistic for 2x2 table (no Yates correction).
    p-value via normal approx of sqrt(chi2) ~ |Z| (rough).

    [KR]
    카이제곱 독립성 검정(2x2):
    - H0: row와 col은 독립
    - H1: 독립이 아니다(연관이 있다)

    p-value는 정확히는 chi-square(df=1) CDF가 필요.
    여기서는 대략적으로 sqrt(chi2)가 |Z|와 유사하다는 근사로 p 계산(참고용).
    """
    n = a + b + c + d
    if n == 0:
        raise ValueError("Counts must sum to > 0.")

    row1 = a + b
    row2 = c + d
    col1 = a + c
    col2 = b + d

    # expected counts
    ea = row1 * col1 / n
    eb = row1 * col2 / n
    ec = row2 * col1 / n
    ed = row2 * col2 / n

    chi2 = 0.0
    for obs, exp in [(a, ea), (b, eb), (c, ec), (d, ed)]:
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp

    # rough approximation: for df=1, chi-square ~ Z^2
    z = math.sqrt(chi2)
    p = two_sided_p_from_z(z)

    v = cramers_v_2x2(a, b, c, d)

    interp = (
        "카이제곱 검정은 범주형 변수 간 독립성을 평가한다. "
        "p-value가 작으면 독립(H0) 가정을 기각할 근거가 있다. "
        "Cramér's V는 연관 강도를 나타내며, 유의하더라도 효과가 작을 수 있다."
    )

    return ChiSquare2x2Result(chi2=float(chi2), p_value_approx=float(p), cramers_v=float(v), interpretation_kr=interp)


# ------------------------------------------------------------
# 6) Permutation test (robust p-value without distribution assumptions)
# ------------------------------------------------------------

@dataclass(frozen=True)
class PermutationTestResult:
    observed_diff: float
    p_value: float
    repeats: int
    interpretation_kr: str


def permutation_test_mean_diff(
    x: Sequence[float],
    y: Sequence[float],
    repeats: int = 5000,
    seed: int = 42
) -> PermutationTestResult:
    """
    Two-sided permutation test for mean difference.

    [KR]
    permutation test:
    - "그룹 라벨이 의미 없다"(H0) 라고 가정하고
      데이터를 섞어가며(mean diff) 분포를 만든 뒤
      관측된 차이가 얼마나 극단적인지로 p-value를 계산.

    장점:
    - 정규성/등분산 같은 분포 가정에 덜 의존
    - 교육/포트폴리오에서 '가정 기반 vs 시뮬레이션 기반' 비교에 매우 좋음
    """
    if len(x) == 0 or len(y) == 0:
        raise ValueError("Samples must be non-empty.")

    rng = random.Random(seed)

    x = list(x)
    y = list(y)
    observed = mean(x) - mean(y)

    combined = x + y
    n1 = len(x)

    extreme = 0
    for _ in range(repeats):
        rng.shuffle(combined)
        x_perm = combined[:n1]
        y_perm = combined[n1:]
        diff = mean(x_perm) - mean(y_perm)
        if abs(diff) >= abs(observed):
            extreme += 1

    # add-one smoothing to avoid p=0
    p = (extreme + 1) / (repeats + 1)

    interp = (
        "Permutation test p-value는 '라벨이 무의미'하다는 H0 하에서 "
        "관측된 평균 차이가 얼마나 극단적인지로 판단한다. "
        "가정이 걱정될 때(정규성/등분산 불명확) 유용하다."
    )

    return PermutationTestResult(observed_diff=float(observed), p_value=float(p), repeats=repeats, interpretation_kr=interp)


# ------------------------------------------------------------
# 7) Demo
# ------------------------------------------------------------

if __name__ == "__main__":
    # 예제 1) 1표본 평균 검정 (정규근사)
    x1 = [52, 50, 49, 51, 50, 48, 53, 49, 50, 51]
    res1 = one_sample_mean_test_normal_approx(x1, mu0=50.0)
    print("\n[One-sample mean test]")
    print(res1)

    # 예제 2) 2표본 평균 차이 (Welch, 정규근사) + 효과크기
    group_a = [10.2, 9.8, 10.1, 10.5, 9.7, 10.0, 10.4]
    group_b = [9.1, 9.3, 9.0, 9.4, 9.2, 9.1, 9.5]
    res2 = welch_t_test_normal_approx(group_a, group_b)
    print("\n[Two-sample Welch test]")
    print(res2)

    # permutation test로 p-value 보완
    perm = permutation_test_mean_diff(group_a, group_b, repeats=5000, seed=2026)
    print("\n[Permutation test for mean difference]")
    print(perm)

    # 예제 3) 2x2 카이제곱 독립성 검정(근사) + Cramér's V
    # 예: A/B 두 그룹과 Yes/No 반응
    a, b, c, d = 30, 20, 15, 35
    chi = chi_square_2x2_normal_approx(a, b, c, d)
    print("\n[Chi-square independence test (2x2)]")
    print(chi)

    print("\n[Notes]")
    print("- p-value는 근사값이므로, 정확한 계산이 필요하면 SciPy 사용을 권장한다.")
    print("- 실무/연구에서는 항상 효과크기(effect size)와 함께 해석하는 습관이 중요하다.")