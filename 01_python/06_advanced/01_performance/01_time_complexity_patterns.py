"""
Day 72 — Time Complexity Patterns
File: 01_python/06_advanced/01_performance/01_time_complexity_patterns.py

목표
- 알고리즘 성능을 분석할 때 사용하는 시간복잡도(Time Complexity) 개념을 이해한다.
- Big-O 표기법을 실전 코드 예시와 함께 익힌다.
- O(1), O(n), O(n^2), O(log n) 대표 패턴을 구현한다.
- 간단한 실행 시간 측정을 통해 성능 차이를 직관적으로 확인한다.

한국어 설명
시간복잡도는 "입력 크기가 커질 때 실행 시간이 어떻게 증가하는가"를 설명하는 방식이다.

예:
- O(1): 입력이 커져도 거의 일정
- O(n): 데이터가 2배면 시간도 대체로 2배
- O(n^2): 데이터가 2배면 시간은 대체로 4배
- O(log n): 매우 천천히 증가

중요:
시간복잡도는 "정확한 실행 시간"이 아니라
"성장 패턴(growth pattern)"을 보는 개념이다.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Iterable, List


# ============================================================
# 0) Utility
# ============================================================

@dataclass(frozen=True)
class BenchmarkResult:
    label: str
    elapsed_seconds: float


def benchmark(func: Callable, *args, repeat: int = 1, label: str | None = None, **kwargs) -> BenchmarkResult:
    """
    간단한 실행 시간 측정 함수

    한국어 설명
    - perf_counter()를 사용해 함수 실행 시간을 측정
    - repeat를 여러 번 주면 반복 실행 후 총 시간 측정 가능
    """
    start = perf_counter()

    for _ in range(repeat):
        func(*args, **kwargs)

    end = perf_counter()

    return BenchmarkResult(
        label=label or func.__name__,
        elapsed_seconds=end - start
    )


# ============================================================
# 1) O(1) — Constant Time
# ============================================================

def get_first_element(data: List[int]) -> int:
    """
    O(1) 예시
    리스트의 첫 번째 요소 접근

    한국어 설명
    - data 크기가 10이든 1,000,000이든
      첫 번째 요소 접근은 거의 일정한 비용이다.
    """
    return data[0]


# ============================================================
# 2) O(n) — Linear Time
# ============================================================

def linear_search(data: List[int], target: int) -> int:
    """
    O(n) 예시
    앞에서부터 하나씩 확인하는 선형 탐색

    한국어 설명
    - 최악의 경우 모든 원소를 다 확인해야 한다.
    - 데이터가 커질수록 실행 시간이 선형적으로 증가한다.
    """
    for idx, value in enumerate(data):
        if value == target:
            return idx
    return -1


def sum_all_elements(data: List[int]) -> int:
    """
    O(n) 예시
    모든 원소를 한 번씩 방문하여 합계 계산
    """
    total = 0
    for value in data:
        total += value
    return total


# ============================================================
# 3) O(n^2) — Quadratic Time
# ============================================================

def count_all_pairs(data: List[int]) -> int:
    """
    O(n^2) 예시
    모든 가능한 (i, j) 쌍의 개수를 센다.

    한국어 설명
    - 중첩 반복문(nested loop)의 대표적인 예
    - 데이터가 커질수록 비용이 급격히 증가한다.
    """
    pair_count = 0

    for _ in data:
        for _ in data:
            pair_count += 1

    return pair_count


def has_duplicate_bruteforce(data: List[int]) -> bool:
    """
    O(n^2) 예시
    모든 쌍을 비교하여 중복 존재 여부 확인

    한국어 설명
    - 비효율적인 중복 탐지 방법
    - 학습용으로는 좋지만 실무에서는 set 활용이 더 낫다.
    """
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j]:
                return True
    return False


# ============================================================
# 4) O(log n) — Logarithmic Time
# ============================================================

def binary_search(sorted_data: List[int], target: int) -> int:
    """
    O(log n) 예시
    이진 탐색(binary search)

    전제:
    - 데이터가 정렬되어 있어야 한다.

    한국어 설명
    - 한 번 비교할 때마다 탐색 구간을 절반으로 줄인다.
    - 데이터가 매우 커도 증가 속도가 완만하다.
    """
    left = 0
    right = len(sorted_data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = sorted_data[mid]

        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# ============================================================
# 5) Better Pattern Example — O(n) vs O(1) average membership
# ============================================================

def membership_in_list(data: List[int], target: int) -> bool:
    """
    리스트 membership 검사

    한국어 설명
    - list에서 target in data는 일반적으로 O(n)
    """
    return target in data


def membership_in_set(data: Iterable[int], target: int) -> bool:
    """
    set membership 검사

    한국어 설명
    - set에서 target in data는 평균적으로 O(1)에 가깝다.
    - membership 확인이 많다면 list보다 set이 훨씬 효율적이다.
    """
    data_set = set(data)
    return target in data_set


# ============================================================
# 6) Demo / Benchmark
# ============================================================

def print_big_o_summary() -> None:
    """
    시간복잡도 요약 출력
    """
    print("=== Time Complexity Summary ===")
    print("O(1)   : constant time")
    print("O(log n): logarithmic time")
    print("O(n)   : linear time")
    print("O(n^2) : quadratic time")
    print()


def run_examples() -> None:
    """
    대표 예시 실행
    """
    data_small = [10, 20, 30, 40, 50]
    data_sorted = [1, 3, 5, 7, 9, 11, 13, 15]

    print("=== Example Outputs ===")
    print("First element (O(1)):", get_first_element(data_small))
    print("Linear search index (O(n)):", linear_search(data_small, 40))
    print("Sum all elements (O(n)):", sum_all_elements(data_small))
    print("All pairs count (O(n^2)):", count_all_pairs(data_small))
    print("Binary search index (O(log n)):", binary_search(data_sorted, 11))
    print("Has duplicate bruteforce (O(n^2)):", has_duplicate_bruteforce([1, 2, 3, 2]))
    print()


def run_benchmarks() -> None:
    """
    간단한 benchmark 실행

    한국어 설명
    - 아주 정밀한 실험은 아니고
      복잡도 차이를 직관적으로 느끼기 위한 예시
    """
    n = 20_000
    data = list(range(n))
    target = n - 1

    # O(1)
    result_o1 = benchmark(get_first_element, data, repeat=50_000, label="O(1) get_first_element")

    # O(n)
    result_on = benchmark(linear_search, data, target, repeat=100, label="O(n) linear_search")

    # O(log n)
    result_ologn = benchmark(binary_search, data, target, repeat=10_000, label="O(log n) binary_search")

    # membership 비교
    result_list_in = benchmark(membership_in_list, data, target, repeat=200, label="O(n) list membership")
    result_set_in = benchmark(membership_in_set, data, target, repeat=200, label="O(1) avg set membership")

    # O(n^2)는 너무 큰 n에서 매우 느려질 수 있으므로 작게 측정
    n_small = 1000
    data_small = list(range(n_small))
    result_on2 = benchmark(count_all_pairs, data_small, repeat=1, label="O(n^2) count_all_pairs")

    results = [
        result_o1,
        result_ologn,
        result_on,
        result_list_in,
        result_set_in,
        result_on2,
    ]

    print("=== Benchmark Results ===")
    for r in results:
        print(f"{r.label:<30} -> {r.elapsed_seconds:.6f} sec")
    print()

    print("=== Interpretation ===")
    print("- O(1)은 입력 크기 증가에 거의 영향이 없다.")
    print("- O(log n)은 매우 큰 데이터에도 비교적 빠르다.")
    print("- O(n)은 데이터를 끝까지 볼 수 있어 점진적으로 느려진다.")
    print("- O(n^2)은 데이터가 커질수록 급격히 느려진다.")
    print("- membership 검사는 list보다 set이 유리한 경우가 많다.")
    print()


# ============================================================
# 7) Main
# ============================================================

def main() -> None:
    print_big_o_summary()
    run_examples()
    run_benchmarks()


if __name__ == "__main__":
    main()