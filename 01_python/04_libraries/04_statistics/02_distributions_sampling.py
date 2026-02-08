"""
Day 35: Distributions & Sampling (확률분포와 샘플링)

[EN]
This file builds intuition for probability distributions and sampling:
- Simulate common distributions (Normal, Binomial, Poisson)
- Compute sample statistics and visualize behavior numerically
- Demonstrate the idea behind the Central Limit Theorem (CLT) via sampling means

[KR]
이 파일은 확률분포와 샘플링을 "시뮬레이션"으로 직관화한다.
- 대표 분포(정규/이항/포아송) 샘플링
- 표본 통계량(평균/분산/표준편차) 계산
- 표본평균의 분포가 정규에 가까워지는 CLT 아이디어를 실험적으로 확인

✅ 외부 라이브러리 없이 실행 가능 (random/statistics 기반)
✅ NumPy가 설치되어 있으면 더 빠른 샘플링 옵션도 제공
"""

from __future__ import annotations

import math
import random
import statistics as stats
from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence, Tuple, Optional


# ---------------------------
# 1) Helper: Summary statistics
# ---------------------------

@dataclass(frozen=True)
class SampleSummary:
    n: int
    mean: float
    stdev: float
    min: float
    max: float
    q1: float
    median: float
    q3: float


def percentile(sorted_x: Sequence[float], p: float) -> float:
    """Linear-interpolated percentile. sorted_x must be sorted and non-empty."""
    if not (0 <= p <= 100):
        raise ValueError("p must be in [0, 100].")
    n = len(sorted_x)
    if n == 0:
        raise ValueError("sorted_x must be non-empty.")
    pos = (n - 1) * (p / 100.0)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    if lo == hi:
        return float(sorted_x[lo])
    w = pos - lo
    return float(sorted_x[lo] * (1 - w) + sorted_x[hi] * w)


def summarize(x: Sequence[float]) -> SampleSummary:
    """Compute robust summary for a numeric sample."""
    if len(x) == 0:
        raise ValueError("Sample is empty.")
    xs = sorted(x)
    n = len(xs)
    mean = float(sum(xs) / n)
    stdev = float(stats.stdev(xs)) if n >= 2 else 0.0
    return SampleSummary(
        n=n,
        mean=mean,
        stdev=stdev,
        min=float(xs[0]),
        max=float(xs[-1]),
        q1=percentile(xs, 25),
        median=float(stats.median(xs)),
        q3=percentile(xs, 75),
    )


def print_summary(title: str, s: SampleSummary) -> None:
    """Pretty print summary (콘솔 출력용)."""
    print(f"\n=== {title} ===")
    print(f"n      : {s.n}")
    print(f"mean   : {s.mean:.4f}")
    print(f"stdev  : {s.stdev:.4f}")
    print(f"min/max: {s.min:.4f} / {s.max:.4f}")
    print(f"Q1     : {s.q1:.4f}")
    print(f"median : {s.median:.4f}")
    print(f"Q3     : {s.q3:.4f}")


# ---------------------------
# 2) Simulators for distributions
# ---------------------------

def sample_normal(mu: float, sigma: float, n: int, seed: Optional[int] = None) -> List[float]:
    """
    Normal(mu, sigma) using random.gauss.

    [KR]
    정규분포 N(mu, sigma^2) 샘플 생성.
    random.gauss(mu, sigma)를 사용한다.
    """
    if sigma <= 0:
        raise ValueError("sigma must be > 0.")
    if n <= 0:
        raise ValueError("n must be > 0.")
    rng = random.Random(seed)
    return [rng.gauss(mu, sigma) for _ in range(n)]


def sample_binomial(trials: int, p: float, n: int, seed: Optional[int] = None) -> List[int]:
    """
    Binomial(trials, p) via repeated Bernoulli trials.

    [KR]
    이항분포 Binomial(trials, p) 샘플 생성.
    - trials번의 베르누이 시행을 합산해 생성 (직관적 구현)
    """
    if trials <= 0:
        raise ValueError("trials must be > 0.")
    if not (0 <= p <= 1):
        raise ValueError("p must be in [0, 1].")
    if n <= 0:
        raise ValueError("n must be > 0.")
    rng = random.Random(seed)

    out: List[int] = []
    for _ in range(n):
        successes = 0
        for _ in range(trials):
            if rng.random() < p:
                successes += 1
        out.append(successes)
    return out


def sample_poisson(lam: float, n: int, seed: Optional[int] = None) -> List[int]:
    """
    Poisson(lam) using Knuth's algorithm.

    [KR]
    포아송분포 Poisson(lam) 샘플 생성.
    - Knuth 알고리즘(전통적인 시뮬레이션 방법)을 사용한다.
    - lam이 너무 크면(예: 1000+) 느려질 수 있으므로 주의.
    """
    if lam <= 0:
        raise ValueError("lam must be > 0.")
    if n <= 0:
        raise ValueError("n must be > 0.")
    rng = random.Random(seed)

    out: List[int] = []
    L = math.exp(-lam)
    for _ in range(n):
        k = 0
        prod = 1.0
        while prod > L:
            k += 1
            prod *= rng.random()
        out.append(k - 1)
    return out


# ---------------------------
# 3) Sampling experiment: CLT intuition
# ---------------------------

def sample_means(
    generator: Callable[[int], List[float]],
    sample_size: int,
    repeats: int,
    seed: Optional[int] = None
) -> List[float]:
    """
    Draw many samples and compute their means.

    [KR]
    여러 번 샘플을 뽑아 "표본평균"을 반복 계산한다.
    CLT(중심극한정리) 직관:
    - 모집단 분포가 정규가 아니어도,
      표본 크기가 커지면 표본평균의 분포가 정규에 가까워진다.
    """
    if sample_size <= 0:
        raise ValueError("sample_size must be > 0.")
    if repeats <= 0:
        raise ValueError("repeats must be > 0.")

    rng = random.Random(seed)
    means: List[float] = []
    for _ in range(repeats):
        # 각 반복에서 seed를 조금씩 바꿔 재현성을 유지하면서 다양성 확보
        s = generator(sample_size) if seed is None else generator(sample_size)
        means.append(float(sum(s) / len(s)))
    return means


def histogram_counts(x: Sequence[float], bins: int = 10) -> List[Tuple[Tuple[float, float], int]]:
    """
    Simple histogram counts (text-based).

    [KR]
    간단한 히스토그램(텍스트 기반) bin 카운트.
    그래프 라이브러리 없이도 분포 형태를 감각적으로 볼 수 있다.
    """
    if len(x) == 0:
        return []
    if bins <= 0:
        raise ValueError("bins must be > 0.")

    xmin, xmax = min(x), max(x)
    if xmin == xmax:
        return [((xmin, xmax), len(x))]

    width = (xmax - xmin) / bins
    counts = [0] * bins
    for v in x:
        idx = int((v - xmin) / width)
        if idx == bins:
            idx -= 1
        counts[idx] += 1

    out: List[Tuple[Tuple[float, float], int]] = []
    for i, c in enumerate(counts):
        lo = xmin + i * width
        hi = xmin + (i + 1) * width
        out.append(((lo, hi), c))
    return out


def print_histogram(title: str, x: Sequence[float], bins: int = 12, width: int = 40) -> None:
    """
    Print a text histogram.

    [KR]
    텍스트 히스토그램 출력(가벼운 시각화).
    """
    print(f"\n--- {title} (hist) ---")
    h = histogram_counts(x, bins=bins)
    if not h:
        print("(empty)")
        return
    max_count = max(c for _, c in h)
    for (lo, hi), c in h:
        bar_len = int((c / max_count) * width) if max_count > 0 else 0
        bar = "#" * bar_len
        print(f"{lo:>8.3f} ~ {hi:>8.3f} | {bar} {c}")


# ---------------------------
# 4) Optional: NumPy acceleration (if available)
# ---------------------------

def try_numpy_sampling() -> bool:
    """
    Try NumPy sampling if NumPy exists.
    [KR] NumPy가 있으면 훨씬 빠르고 간결하게 샘플 생성 가능.
    """
    try:
        import numpy as np  # type: ignore
    except Exception:
        return False

    rng = np.random.default_rng(42)
    x = rng.normal(loc=0.0, scale=1.0, size=100_000)
    s = SampleSummary(
        n=len(x),
        mean=float(x.mean()),
        stdev=float(x.std(ddof=1)),
        min=float(x.min()),
        max=float(x.max()),
        q1=float(np.percentile(x, 25)),
        median=float(np.percentile(x, 50)),
        q3=float(np.percentile(x, 75)),
    )
    print_summary("NumPy Normal(0,1) demo (n=100000)", s)
    return True


# ---------------------------
# 5) Main demo
# ---------------------------

if __name__ == "__main__":
    # 재현성을 위한 seed 설정 (원하면 바꿔도 OK)
    SEED = 2026

    # 1) Normal distribution
    normal_sample = sample_normal(mu=10.0, sigma=2.0, n=5000, seed=SEED)
    print_summary("Normal(mu=10, sigma=2) sample", summarize(normal_sample))
    print_histogram("Normal(mu=10, sigma=2)", normal_sample, bins=14)

    # 2) Binomial distribution
    # 예: trials=20번 시행, 성공확률 p=0.3
    binom_sample = sample_binomial(trials=20, p=0.3, n=5000, seed=SEED)
    # int 리스트도 summarize 가능하도록 float로 변환
    print_summary("Binomial(trials=20, p=0.3) sample", summarize([float(v) for v in binom_sample]))
    print_histogram("Binomial(trials=20, p=0.3)", [float(v) for v in binom_sample], bins=15)

    # 3) Poisson distribution
    # 예: 평균 발생률 lam=4
    pois_sample = sample_poisson(lam=4.0, n=5000, seed=SEED)
    print_summary("Poisson(lam=4) sample", summarize([float(v) for v in pois_sample]))
    print_histogram("Poisson(lam=4)", [float(v) for v in pois_sample], bins=14)

    # 4) CLT intuition: sample means
    # [KR] 모집단이 "비대칭(포아송)"인 경우에도,
    #      표본평균은 표본크기가 커질수록 정규형태에 가까워지는 경향을 보인다.
    def poisson_generator(k: int) -> List[float]:
        return [float(v) for v in sample_poisson(lam=4.0, n=k, seed=None)]

    means_n5 = [sum(poisson_generator(5)) / 5 for _ in range(2000)]
    means_n30 = [sum(poisson_generator(30)) / 30 for _ in range(2000)]

    print_summary("CLT demo (Poisson lam=4) - means of n=5", summarize(means_n5))
    print_histogram("Means (n=5)", means_n5, bins=14)

    print_summary("CLT demo (Poisson lam=4) - means of n=30", summarize(means_n30))
    print_histogram("Means (n=30)", means_n30, bins=14)

    # 5) Optional NumPy demo
    used_numpy = try_numpy_sampling()
    if not used_numpy:
        print("\n[Note] NumPy not found. Standard library simulation was used.")