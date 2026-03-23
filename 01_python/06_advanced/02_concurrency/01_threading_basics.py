"""
Day 75 — Threading Basics
File: 01_python/06_advanced/02_concurrency/01_threading_basics.py

목표
- Python의 threading 기본 개념을 이해한다.
- Thread 생성, 시작(start), 종료 대기(join) 방법을 익힌다.
- I/O 성격의 작업에서 threading이 왜 유용한지 감각을 익힌다.
- 공유 자원(shared state) 접근 시 Lock이 왜 필요한지 기초를 배운다.

핵심 개념
1) Thread
   - 하나의 프로세스 안에서 동시에 실행되는 작업 흐름

2) start()
   - 스레드 실행 시작

3) join()
   - 해당 스레드가 끝날 때까지 기다림

4) Shared State
   - 여러 스레드가 함께 접근하는 데이터
   - 경쟁 상태(race condition)가 발생할 수 있음

5) Lock
   - 공유 자원을 안전하게 다루기 위한 동기화 도구

한국어 설명
threading은 "여러 일을 동시에 처리하는 구조"를 배우는 첫 단계다.

특히 Python에서 threading은
CPU를 강하게 쓰는 계산보다는
네트워크 요청, 파일 읽기/쓰기, 대기 시간이 있는 작업처럼
I/O 중심 작업에서 더 유용한 경우가 많다.
"""

from __future__ import annotations

import threading
import time
from typing import List


# ============================================================
# 0) Basic Worker Function
# ============================================================

def worker(task_name: str, delay: float) -> None:
    """
    가장 기본적인 worker 함수

    한국어 설명
    - task_name: 작업 이름
    - delay: 몇 초 동안 대기할지
    - time.sleep()은 실제 I/O는 아니지만, 대기 작업을 흉내 내는 데 자주 사용한다.
    """
    current_thread = threading.current_thread().name

    print(f"[START] {task_name} started on thread={current_thread}")
    time.sleep(delay)
    print(f"[END]   {task_name} finished on thread={current_thread}")


# ============================================================
# 1) Thread Creation Basics
# ============================================================

def demo_basic_threads() -> None:
    """
    기본적인 스레드 생성 / 시작 / 종료 대기 예시
    """
    print("\n=== Demo 1: Basic Thread Creation ===")

    t1 = threading.Thread(target=worker, args=("task_A", 1.5), name="worker-A")
    t2 = threading.Thread(target=worker, args=("task_B", 1.0), name="worker-B")

    # 한국어 설명
    # start()를 호출해야 실제 스레드 실행이 시작된다.
    t1.start()
    t2.start()

    print("[MAIN] Waiting for threads to finish...")

    # 한국어 설명
    # join()은 해당 스레드가 끝날 때까지 메인 스레드를 대기시킨다.
    t1.join()
    t2.join()

    print("[MAIN] All basic threads completed.")


# ============================================================
# 2) Multiple I/O-like Tasks
# ============================================================

def io_like_task(task_id: int, results: List[str]) -> None:
    """
    I/O 같은 대기 작업을 흉내 내는 예시

    한국어 설명
    - 실제 웹 요청 대신 sleep으로 대기
    - 결과를 results 리스트에 기록
    """
    current_thread = threading.current_thread().name
    print(f"[IO] task_id={task_id} running on {current_thread}")

    time.sleep(1.0)

    result = f"result_from_task_{task_id}"
    results.append(result)

    print(f"[IO] task_id={task_id} finished on {current_thread}")


def demo_multiple_threads() -> None:
    """
    여러 개의 I/O-like 작업을 동시에 실행하는 예시
    """
    print("\n=== Demo 2: Multiple I/O-like Tasks ===")

    threads: List[threading.Thread] = []
    results: List[str] = []

    start_time = time.perf_counter()

    for task_id in range(1, 6):
        thread = threading.Thread(
            target=io_like_task,
            args=(task_id, results),
            name=f"io-worker-{task_id}"
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start_time

    print("[MAIN] Results:", results)
    print(f"[MAIN] Elapsed time: {elapsed:.2f} seconds")

    # 한국어 설명
    # 각 작업이 1초씩 걸려도, 순차 실행보다 더 빠르게 끝나는 모습을 관찰할 수 있다.
    # 이는 threading이 대기 시간이 있는 작업에서 유용할 수 있음을 보여준다.


# ============================================================
# 3) Shared State Example
# ============================================================

shared_counter = 0


def increment_counter_unsafe(n: int) -> None:
    """
    Lock 없이 공유 변수 증가

    한국어 설명
    - 교육용 예시
    - race condition 위험이 있다는 점을 설명하기 위한 코드
    - 환경/타이밍에 따라 항상 문제가 재현되지는 않을 수 있음
    """
    global shared_counter

    for _ in range(n):
        shared_counter += 1


def demo_shared_state_unsafe() -> None:
    """
    공유 상태를 Lock 없이 다루는 예시
    """
    print("\n=== Demo 3: Shared State Without Lock ===")

    global shared_counter
    shared_counter = 0

    t1 = threading.Thread(target=increment_counter_unsafe, args=(100_000,), name="unsafe-1")
    t2 = threading.Thread(target=increment_counter_unsafe, args=(100_000,), name="unsafe-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"[MAIN] shared_counter (unsafe) = {shared_counter}")
    print(
        "[MAIN] Note: Without a lock, shared state access can be unsafe "
        "even if the issue is not always visibly reproduced."
    )


# ============================================================
# 4) Lock Basics
# ============================================================

safe_counter = 0
counter_lock = threading.Lock()


def increment_counter_safe(n: int) -> None:
    """
    Lock을 사용한 공유 변수 증가

    한국어 설명
    - with counter_lock:
      해당 블록은 한 번에 하나의 스레드만 들어갈 수 있다.
    """
    global safe_counter

    for _ in range(n):
        with counter_lock:
            safe_counter += 1


def demo_shared_state_safe() -> None:
    """
    Lock을 사용한 안전한 공유 상태 처리 예시
    """
    print("\n=== Demo 4: Shared State With Lock ===")

    global safe_counter
    safe_counter = 0

    t1 = threading.Thread(target=increment_counter_safe, args=(100_000,), name="safe-1")
    t2 = threading.Thread(target=increment_counter_safe, args=(100_000,), name="safe-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"[MAIN] safe_counter (with lock) = {safe_counter}")


# ============================================================
# 5) Thread Information
# ============================================================

def demo_thread_metadata() -> None:
    """
    현재 스레드 정보 확인
    """
    print("\n=== Demo 5: Thread Metadata ===")

    main_thread = threading.current_thread()
    print(f"[MAIN] Main thread name: {main_thread.name}")
    print(f"[MAIN] Active thread count (approx): {threading.active_count()}")


# ============================================================
# 6) Main
# ============================================================

def main() -> None:
    """
    전체 데모 실행
    """
    demo_thread_metadata()
    demo_basic_threads()
    demo_multiple_threads()
    demo_shared_state_unsafe()
    demo_shared_state_safe()

    print("\n=== Summary ===")
    print("1. threading.Thread로 작업을 병렬적으로 실행할 수 있다.")
    print("2. start()는 실행 시작, join()은 종료 대기다.")
    print("3. 대기 시간이 있는 작업에서는 threading이 유용할 수 있다.")
    print("4. 공유 상태를 다룰 때는 Lock 같은 동기화 도구가 중요하다.")


if __name__ == "__main__":
    main()