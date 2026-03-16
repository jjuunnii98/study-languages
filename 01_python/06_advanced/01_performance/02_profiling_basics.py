"""
Day 73 — Profiling Basics
File: 01_python/06_advanced/01_performance/02_profiling_basics.py

목표
- Python 코드의 병목 구간을 찾는 기본 방법을 익힌다.
- 단순 시간 측정(time.perf_counter)과 프로파일링(cProfile)의 차이를 이해한다.
- 어떤 함수가 오래 걸리는지, 몇 번 호출되는지 확인하는 감각을 기른다.

핵심 개념
1) Timing
   - 특정 코드 블록의 실행 시간을 직접 측정
   - 빠르게 성능 비교할 때 유용

2) Profiling
   - 함수별 실행 시간 / 호출 횟수 / 누적 시간 분석
   - "어디가 느린가?"를 찾을 때 유용

3) 병목(Bottleneck)
   - 전체 실행 시간을 가장 많이 잡아먹는 부분
   - 최적화는 병목부터 해야 의미가 있다

한국어 설명
성능 최적화에서 가장 흔한 실수는
"느릴 것 같은 부분을 감으로 고치는 것"이다.

실무에서는 먼저 측정하고,
그다음 병목을 찾고,
그다음 최적화해야 한다.
"""

from __future__ import annotations

import cProfile
import io
import pstats
from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Iterable, List


# ============================================================
# 0) Benchmark Utility
# ============================================================

@dataclass(frozen=True)
class TimingResult:
    label: str
    elapsed_seconds: float


def measure_time(func: Callable, *args, repeat: int = 1, label: str | None = None, **kwargs) -> TimingResult:
    """
    간단한 실행 시간 측정 함수

    한국어 설명
    - perf_counter()는 고해상도 타이머
    - 빠른 비교 실험에 적합
    """
    start = perf_counter()

    for _ in range(repeat):
        func(*args, **kwargs)

    end = perf_counter()

    return TimingResult(
        label=label or func.__name__,
        elapsed_seconds=end - start
    )


# ============================================================
# 1) Example A — String Building
# ============================================================

def build_string_slow(n: int) -> str:
    """
    비효율적인 문자열 누적 예시

    한국어 설명
    - 반복문에서 문자열을 계속 더하는 방식
    - 작은 규모에서는 괜찮아 보일 수 있지만,
      n이 커질수록 비효율적일 수 있다.
    """
    result = ""
    for i in range(n):
        result += str(i)
    return result


def build_string_fast(n: int) -> str:
    """
    더 나은 문자열 결합 예시

    한국어 설명
    - 문자열 조각을 리스트로 모은 뒤
      마지막에 ''.join()으로 합친다.
    - 실무에서 더 자주 추천되는 패턴
    """
    parts = []
    for i in range(n):
        parts.append(str(i))
    return "".join(parts)


# ============================================================
# 2) Example B — Duplicate Detection
# ============================================================

def has_duplicate_bruteforce(data: List[int]) -> bool:
    """
    느린 중복 탐지 예시 (O(n^2))

    한국어 설명
    - 모든 쌍을 비교
    - 입력이 커질수록 급격히 느려짐
    """
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                return True
    return False


def has_duplicate_set(data: Iterable[int]) -> bool:
    """
    더 나은 중복 탐지 예시 (평균적으로 O(n))

    한국어 설명
    - set의 membership 성능을 활용
    - 실무에서 훨씬 일반적인 패턴
    """
    seen = set()
    for value in data:
        if value in seen:
            return True
        seen.add(value)
    return False


# ============================================================
# 3) Example C — Workload Runner
# ============================================================

def run_string_workload(n: int = 10_000) -> None:
    """
    문자열 관련 workload 실행
    """
    build_string_slow(n)
    build_string_fast(n)


def run_duplicate_workload(n: int = 3_000) -> None:
    """
    중복 탐지 workload 실행
    """
    data = list(range(n)) + [n - 1]
    has_duplicate_bruteforce(data)
    has_duplicate_set(data)


# ============================================================
# 4) Simple Timing Comparison
# ============================================================

def run_timing_demo() -> None:
    """
    perf_counter 기반 비교

    한국어 설명
    - 아주 정밀한 실험은 아니고
      두 구현의 상대적 차이를 직관적으로 보는 예시
    """
    print("=== Timing Demo ===")

    string_n = 8_000
    duplicate_n = 2_500

    results = [
        measure_time(build_string_slow, string_n, repeat=5, label="build_string_slow"),
        measure_time(build_string_fast, string_n, repeat=5, label="build_string_fast"),
        measure_time(
            has_duplicate_bruteforce,
            list(range(duplicate_n)) + [duplicate_n - 1],
            repeat=1,
            label="has_duplicate_bruteforce"
        ),
        measure_time(
            has_duplicate_set,
            list(range(duplicate_n)) + [duplicate_n - 1],
            repeat=20,
            label="has_duplicate_set"
        ),
    ]

    for result in results:
        print(f"{result.label:<28} -> {result.elapsed_seconds:.6f} sec")

    print()
    print("=== Timing Interpretation ===")
    print("- 느린 구현과 빠른 구현을 직접 비교할 수 있다.")
    print("- 반복 횟수(repeat)는 함수 속도에 맞게 조절해야 한다.")
    print("- timing은 빠른 비교에 좋지만 함수별 상세 병목은 잘 안 보인다.")
    print()


# ============================================================
# 5) cProfile Helper
# ============================================================

def profile_function(func: Callable, *args, sort_by: str = "cumulative", top_n: int = 15, **kwargs) -> str:
    """
    cProfile 결과를 문자열로 반환

    한국어 설명
    - cProfile: 함수별 호출 시간 분석 도구
    - pstats: 출력 정렬 및 요약 도구
    """
    profiler = cProfile.Profile()
    profiler.enable()

    func(*args, **kwargs)

    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats(sort_by)
    stats.print_stats(top_n)

    return stream.getvalue()


# ============================================================
# 6) Profile Demo
# ============================================================

def run_profile_demo() -> None:
    """
    cProfile 시연

    한국어 설명
    - 어떤 함수가 시간을 많이 쓰는지 본다.
    - tottime / cumtime 개념을 감각적으로 익힌다.
    """
    print("=== cProfile Demo: String Workload ===")
    profile_text_1 = profile_function(run_string_workload, 12_000, sort_by="cumulative", top_n=12)
    print(profile_text_1)

    print("=== cProfile Demo: Duplicate Workload ===")
    profile_text_2 = profile_function(run_duplicate_workload, 2_500, sort_by="cumulative", top_n=12)
    print(profile_text_2)

    print("=== How to Read Profiling Output ===")
    print("- ncalls    : 함수 호출 횟수")
    print("- tottime   : 해당 함수 내부에서 직접 사용한 시간")
    print("- cumtime   : 하위 함수 포함 누적 시간")
    print("- cumtime이 큰 함수부터 보면 전체 병목 파악에 유리하다.")
    print()


# ============================================================
# 7) Optimization Note
# ============================================================

def print_optimization_principles() -> None:
    """
    최적화 원칙 요약
    """
    print("=== Optimization Principles ===")
    print("1. 먼저 측정하고, 나중에 최적화한다.")
    print("2. 병목이 아닌 부분을 고쳐도 체감 개선은 거의 없다.")
    print("3. 알고리즘 개선이 마이크로 최적화보다 효과가 큰 경우가 많다.")
    print("4. list 대신 set, 문자열 누적 대신 join 같은 패턴 차이가 중요하다.")
    print("5. readability와 maintainability도 함께 고려해야 한다.")
    print()


# ============================================================
# 8) Main
# ============================================================

def main() -> None:
    run_timing_demo()
    run_profile_demo()
    print_optimization_principles()


if __name__ == "__main__":
    main()