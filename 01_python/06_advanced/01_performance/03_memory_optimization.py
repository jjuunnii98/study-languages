"""
Day 74 — Memory Optimization
File: 01_python/06_advanced/01_performance/03_memory_optimization.py

목표
- Python에서 메모리를 아끼는 기본 패턴을 이해한다.
- list와 generator의 차이를 비교한다.
- 불필요한 중간 객체 생성을 줄이는 방법을 익힌다.
- 큰 데이터를 "한 번에 다 올리지 않고" 처리하는 사고를 배운다.

핵심 개념
1) Eager Evaluation
   - 리스트처럼 값을 한 번에 모두 메모리에 올리는 방식

2) Lazy Evaluation
   - generator처럼 필요할 때 하나씩 값을 생성하는 방식

3) Intermediate Object
   - 처리 중간에 불필요하게 만들어지는 임시 객체
   - 이런 객체가 많으면 메모리 사용량이 커진다.

4) Chunk Processing
   - 큰 데이터를 나눠서 처리하는 방식
   - 파일 처리 / 로그 처리 / ETL 작업에서 매우 중요

한국어 설명
메모리 최적화는 "코드를 빠르게 만드는 것"과는 약간 다르다.
핵심은 다음 질문이다.

- 지금 모든 데이터를 한꺼번에 메모리에 올려야 하는가?
- 중간 결과를 꼭 리스트로 만들어야 하는가?
- 하나씩 흘려보내면서 처리할 수는 없는가?
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Generator, Iterable, Iterator, List


# ============================================================
# 0) Utility
# ============================================================

@dataclass(frozen=True)
class MemoryCheckResult:
    label: str
    object_type: str
    size_bytes: int


def inspect_size(obj: object, label: str) -> MemoryCheckResult:
    """
    객체의 대략적인 크기 확인

    한국어 설명
    - sys.getsizeof()는 "객체 자체"의 크기를 보여준다.
    - 내부 원소 전체를 완벽히 합산한 총메모리는 아닐 수 있다.
    - 그래도 list vs generator 비교에는 충분히 유용하다.
    """
    return MemoryCheckResult(
        label=label,
        object_type=type(obj).__name__,
        size_bytes=sys.getsizeof(obj),
    )


def print_size_report(*results: MemoryCheckResult) -> None:
    """
    메모리 비교 출력
    """
    print("=== Memory Size Report ===")
    for r in results:
        print(f"{r.label:<28} | type={r.object_type:<15} | size={r.size_bytes} bytes")
    print()


# ============================================================
# 1) List vs Generator
# ============================================================

def build_number_list(n: int) -> List[int]:
    """
    모든 숫자를 리스트로 한 번에 생성

    한국어 설명
    - n이 커질수록 메모리를 많이 사용
    - eager evaluation 방식
    """
    return [i for i in range(n)]


def build_number_generator(n: int) -> Generator[int, None, None]:
    """
    숫자를 필요할 때 하나씩 생성

    한국어 설명
    - generator는 값을 한 번에 다 만들지 않는다.
    - lazy evaluation 방식
    """
    for i in range(n):
        yield i


# ============================================================
# 2) Intermediate Object Example
# ============================================================

def square_even_numbers_list(data: Iterable[int]) -> List[int]:
    """
    비효율적인 예시: 중간 리스트 생성 가능성 높음

    한국어 설명
    - 조건 필터링 후 결과를 리스트로 모은다.
    - 데이터가 크면 메모리 사용량이 커질 수 있다.
    """
    return [x * x for x in data if x % 2 == 0]


def square_even_numbers_generator(data: Iterable[int]) -> Generator[int, None, None]:
    """
    더 나은 예시: generator 사용

    한국어 설명
    - 결과를 한 번에 다 저장하지 않고 하나씩 반환
    """
    for x in data:
        if x % 2 == 0:
            yield x * x


# ============================================================
# 3) Chunk Processing
# ============================================================

def chunked(data: List[int], chunk_size: int) -> Iterator[List[int]]:
    """
    데이터를 chunk 단위로 나누어 반환

    한국어 설명
    - 큰 데이터를 한 번에 처리하지 않고 나눠서 처리
    - 실무에서 파일, 로그, DB fetch, ETL에 자주 사용
    """
    for start in range(0, len(data), chunk_size):
        end = start + chunk_size
        yield data[start:end]


def process_chunks(data: List[int], chunk_size: int = 1000) -> int:
    """
    chunk 단위 처리 예시
    - 짝수의 합 계산
    """
    total = 0

    for chunk in chunked(data, chunk_size):
        for value in chunk:
            if value % 2 == 0:
                total += value

    return total


# ============================================================
# 4) String Memory Pattern
# ============================================================

def build_strings_list(n: int) -> List[str]:
    """
    문자열 리스트를 한 번에 생성
    """
    return [f"user_{i}" for i in range(n)]


def build_strings_generator(n: int) -> Generator[str, None, None]:
    """
    문자열을 하나씩 생성
    """
    for i in range(n):
        yield f"user_{i}"


# ============================================================
# 5) Demo Functions
# ============================================================

def demo_list_vs_generator() -> None:
    """
    list와 generator 메모리 비교
    """
    n = 100_000

    number_list = build_number_list(n)
    number_generator = build_number_generator(n)

    list_size = inspect_size(number_list, "number_list")
    generator_size = inspect_size(number_generator, "number_generator")

    print("=== Demo 1: List vs Generator ===")
    print_size_report(list_size, generator_size)

    # generator는 일부만 소비 가능
    print("First 5 values from generator:")
    gen_preview = build_number_generator(5)
    for value in gen_preview:
        print(value, end=" ")
    print("\n")


def demo_intermediate_objects() -> None:
    """
    중간 객체 생성 차이 예시
    """
    data = list(range(50_000))

    result_list = square_even_numbers_list(data)
    result_generator = square_even_numbers_generator(data)

    list_size = inspect_size(result_list, "square_even_list")
    generator_size = inspect_size(result_generator, "square_even_generator")

    print("=== Demo 2: Intermediate Objects ===")
    print_size_report(list_size, generator_size)

    # generator는 실제 소비할 때 값 생성
    print("First 5 values from square_even_generator:")
    gen = square_even_numbers_generator(range(20))
    for _ in range(5):
        print(next(gen), end=" ")
    print("\n")


def demo_chunk_processing() -> None:
    """
    chunk processing 예시
    """
    data = list(range(100_000))

    print("=== Demo 3: Chunk Processing ===")
    total = process_chunks(data, chunk_size=5000)
    print(f"Sum of even numbers (chunk processing): {total}")
    print("Chunk processing allows large data to be handled in smaller pieces.\n")


def demo_string_memory() -> None:
    """
    문자열 생성 메모리 비교
    """
    n = 50_000

    string_list = build_strings_list(n)
    string_generator = build_strings_generator(n)

    list_size = inspect_size(string_list, "string_list")
    generator_size = inspect_size(string_generator, "string_generator")

    print("=== Demo 4: String Generation ===")
    print_size_report(list_size, generator_size)


# ============================================================
# 6) Practical Notes
# ============================================================

def print_memory_optimization_notes() -> None:
    """
    메모리 최적화 핵심 원칙 출력
    """
    print("=== Memory Optimization Principles ===")
    print("1. 모든 데이터를 한 번에 리스트로 만들 필요가 있는지 먼저 생각한다.")
    print("2. 순차 처리 가능하면 generator를 고려한다.")
    print("3. 중간 리스트/중간 객체를 불필요하게 만들지 않는다.")
    print("4. 큰 데이터는 chunk 단위로 나눠 처리한다.")
    print("5. 메모리 최적화는 파일 처리, 로그 처리, ETL, ML preprocessing에 특히 중요하다.")
    print()


# ============================================================
# 7) Main
# ============================================================

def main() -> None:
    demo_list_vs_generator()
    demo_intermediate_objects()
    demo_chunk_processing()
    demo_string_memory()
    print_memory_optimization_notes()


if __name__ == "__main__":
    main()