"""
Day 34: Descriptive Statistics (기술 통계)

[EN]
This file covers core descriptive statistics used in data analysis:
- central tendency (mean, median, mode)
- dispersion (variance, standard deviation, range, IQR)
- robust statistics (trimmed mean, MAD)
- simple summary report function

[KR]
이 파일은 데이터 분석에서 가장 자주 쓰는 기술 통계를 다룬다.
- 중심 경향: 평균, 중앙값, 최빈값
- 산포: 분산, 표준편차, 범위, IQR
- 강건 통계: 절사평균(trimmed mean), MAD(중앙값 절대편차)
- 분석에 바로 쓸 수 있는 요약 리포트 함수

※ 외부 라이브러리 없이도 동작하도록 표준 라이브러리 중심으로 작성했고,
  NumPy/Pandas가 있으면 더 편리한 방식도 참고로 포함했다.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum
from typing import Iterable, List, Optional, Sequence, Tuple
import statistics as stats


# ---------------------------
# 1) 데이터 정리 유틸
# ---------------------------

def to_clean_float_list(values: Iterable[object]) -> List[float]:
    """
    Convert mixed values to a clean list of floats.
    - None, "", NaN-like strings are skipped.
    - Non-convertible values are skipped.

    [KR]
    다양한 형태의 입력값을 float 리스트로 변환한다.
    - None, 빈 문자열, NaN처럼 보이는 값은 제외
    - 숫자로 변환 불가한 값도 제외
    """
    cleaned: List[float] = []
    for v in values:
        if v is None:
            continue
        if isinstance(v, str):
            s = v.strip()
            if s == "" or s.lower() in {"nan", "none", "null"}:
                continue
            try:
                cleaned.append(float(s))
            except ValueError:
                continue
        else:
            try:
                cleaned.append(float(v))
            except (TypeError, ValueError):
                continue
    return cleaned


def percentile(sorted_x: Sequence[float], p: float) -> float:
    """
    Compute percentile with linear interpolation.
    Assumes sorted_x is sorted ascending and non-empty.

    [KR]
    정렬된 데이터에서 p 분위수(0~100)를 선형 보간으로 계산.
    - 예: p=25 => 1사분위(Q1), p=50 => 중앙값, p=75 => 3사분위(Q3)
    """
    if not (0 <= p <= 100):
        raise ValueError("p must be in [0, 100].")
    n = len(sorted_x)
    if n == 0:
        raise ValueError("sorted_x must be non-empty.")

    # 위치를 0~(n-1) 인덱스 공간에서 계산
    pos = (n - 1) * (p / 100.0)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    if lo == hi:
        return float(sorted_x[lo])
    weight = pos - lo
    return float(sorted_x[lo] * (1 - weight) + sorted_x[hi] * weight)


def iqr(sorted_x: Sequence[float]) -> float:
    """
    Interquartile range = Q3 - Q1

    [KR]
    IQR(사분위 범위) = Q3 - Q1
    이상치(outlier) 탐지에서 자주 사용되는 강건한 산포 지표.
    """
    q1 = percentile(sorted_x, 25)
    q3 = percentile(sorted_x, 75)
    return q3 - q1


def trimmed_mean(sorted_x: Sequence[float], proportion_to_cut: float = 0.1) -> float:
    """
    Compute trimmed mean by removing extremes from both ends.

    [KR]
    절사평균: 양쪽 끝 일부 비율을 제거하고 평균 계산.
    - outlier의 영향을 줄이기 위한 강건 통계
    """
    if not (0 <= proportion_to_cut < 0.5):
        raise ValueError("proportion_to_cut must be in [0, 0.5).")
    n = len(sorted_x)
    if n == 0:
        raise ValueError("sorted_x must be non-empty.")
    k = int(n * proportion_to_cut)
    trimmed = sorted_x[k:n - k] if n - 2 * k > 0 else sorted_x
    return float(fsum(trimmed) / len(trimmed))


def mad(sorted_x: Sequence[float]) -> float:
    """
    Median Absolute Deviation (MAD): median(|x - median(x)|)

    [KR]
    MAD(중앙값 절대편차): 중앙값 기반의 강건 산포 지표.
    표준편차보다 outlier에 덜 민감하다.
    """
    med = stats.median(sorted_x)
    abs_devs = [abs(x - med) for x in sorted_x]
    abs_devs.sort()
    return float(stats.median(abs_devs))


# ---------------------------
# 2) 기술 통계 요약
# ---------------------------

@dataclass(frozen=True)
class DescriptiveSummary:
    n: int
    mean: float
    median: float
    mode: Optional[float]
    min: float
    max: float
    range: float
    variance_sample: float
    std_sample: float
    q1: float
    q3: float
    iqr: float
    trimmed_mean_10pct: float
    mad: float


def descriptive_summary(values: Iterable[object]) -> DescriptiveSummary:
    """
    Build descriptive summary for numeric data.

    [KR]
    숫자 데이터의 기술 통계 요약을 생성한다.
    - 입력값을 정제(clean)한 후 계산
    - 표본분산/표본표준편차(sample) 기준
    """
    x = to_clean_float_list(values)
    if len(x) == 0:
        raise ValueError("No valid numeric data after cleaning.")
    x.sort()

    n = len(x)
    mean_val = float(fsum(x) / n)
    median_val = float(stats.median(x))

    # mode는 데이터에 따라 예외가 나거나(최빈값 다수/없음) 값이 애매할 수 있음
    mode_val: Optional[float]
    try:
        mode_val = float(stats.mode(x))
    except stats.StatisticsError:
        mode_val = None

    min_val = float(x[0])
    max_val = float(x[-1])
    range_val = max_val - min_val

    # 표본분산/표본표준편차: n>=2 필요
    if n >= 2:
        var_s = float(stats.variance(x))
        std_s = float(stats.stdev(x))
    else:
        var_s = 0.0
        std_s = 0.0

    q1 = percentile(x, 25)
    q3 = percentile(x, 75)
    iqr_val = q3 - q1

    tmean = trimmed_mean(x, 0.1)
    mad_val = mad(x)

    return DescriptiveSummary(
        n=n,
        mean=mean_val,
        median=median_val,
        mode=mode_val,
        min=min_val,
        max=max_val,
        range=range_val,
        variance_sample=var_s,
        std_sample=std_s,
        q1=q1,
        q3=q3,
        iqr=iqr_val,
        trimmed_mean_10pct=tmean,
        mad=mad_val,
    )


# ---------------------------
# 3) 출력(리포트) 도우미
# ---------------------------

def print_summary(title: str, summary: DescriptiveSummary) -> None:
    """
    Print a clean summary report.

    [KR]
    콘솔에서 보기 좋게 요약 출력.
    GitHub에 업로드할 때도 "실행 예시"로 좋은 형태.
    """
    print(f"\n=== {title} ===")
    print(f"n                 : {summary.n}")
    print(f"mean              : {summary.mean:.4f}")
    print(f"median            : {summary.median:.4f}")
    print(f"mode              : {summary.mode if summary.mode is not None else 'None'}")
    print(f"min / max         : {summary.min:.4f} / {summary.max:.4f}")
    print(f"range             : {summary.range:.4f}")
    print(f"variance (sample) : {summary.variance_sample:.4f}")
    print(f"std (sample)      : {summary.std_sample:.4f}")
    print(f"Q1 / Q3           : {summary.q1:.4f} / {summary.q3:.4f}")
    print(f"IQR               : {summary.iqr:.4f}")
    print(f"trimmed mean(10%) : {summary.trimmed_mean_10pct:.4f}")
    print(f"MAD               : {summary.mad:.4f}")


# ---------------------------
# 4) 실행 예시
# ---------------------------

if __name__ == "__main__":
    # 예제 데이터: 이상치 포함
    raw = [10, 12, 12, 13, 14, 100, None, "15", " 16 ", "nan", "oops"]

    summary = descriptive_summary(raw)
    print_summary("Sample Data (with outlier)", summary)

    # IQR 기반 단순 이상치 범위 계산 예시
    # [KR] 실무에서는 IQR 규칙(1.5*IQR)을 자주 사용한다.
    sorted_x = to_clean_float_list(raw)
    sorted_x.sort()
    q1 = percentile(sorted_x, 25)
    q3 = percentile(sorted_x, 75)
    iqr_val = q3 - q1
    lower = q1 - 1.5 * iqr_val
    upper = q3 + 1.5 * iqr_val

    print("\n[IQR Outlier Rule]")
    print(f"lower bound: {lower:.4f}")
    print(f"upper bound: {upper:.4f}")
    outliers = [v for v in sorted_x if v < lower or v > upper]
    print(f"outliers   : {outliers}")