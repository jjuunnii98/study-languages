"""
Day 77 — Asyncio Basics
File: 01_python/06_advanced/02_concurrency/03_asyncio_basics.py

목표
- Python asyncio의 기본 개념을 이해한다.
- async / await 문법을 익힌다.
- asyncio.run(), asyncio.gather(), create_task() 사용법을 배운다.
- 순차 실행과 비동기 동시 실행의 차이를 감각적으로 이해한다.

핵심 개념
1) async def
   - 비동기 코루틴(coroutine) 함수를 정의한다.

2) await
   - 다른 비동기 작업이 끝날 때까지 "협력적으로" 기다린다.

3) event loop
   - 비동기 작업들을 스케줄링하고 실행하는 중심 구조

4) asyncio.run()
   - 최상위 비동기 함수를 실행하는 일반적인 진입점

5) asyncio.gather()
   - 여러 코루틴을 동시에 실행하고 결과를 모은다.

한국어 설명
asyncio는 스레드를 여러 개 만드는 방식이 아니라,
하나의 이벤트 루프 안에서 여러 비동기 작업을 효율적으로 관리하는 방식이다.

특히:
- 네트워크 요청
- API 호출
- 파일 I/O
- 대기 시간이 긴 작업

같은 상황에서 유용한 경우가 많다.
"""

from __future__ import annotations

import asyncio
import time
from typing import List


# ============================================================
# 0) Basic Async Worker
# ============================================================

async def async_worker(task_name: str, delay: float) -> str:
    """
    가장 기본적인 비동기 worker

    한국어 설명
    - asyncio.sleep()은 time.sleep()과 다르다.
    - 이벤트 루프를 막지 않고 "기다리는 동안 다른 작업이 실행될 수 있게" 한다.
    """
    print(f"[START] {task_name} started (delay={delay})")
    await asyncio.sleep(delay)
    print(f"[END]   {task_name} finished")
    return f"{task_name}_done"


# ============================================================
# 1) Sequential vs Concurrent
# ============================================================

async def run_sequential() -> List[str]:
    """
    순차 실행 예시

    한국어 설명
    - 작업을 하나씩 await 하므로 전체 시간이 더 오래 걸릴 수 있다.
    """
    print("\n=== Demo 1: Sequential Async Execution ===")

    start = time.perf_counter()

    result1 = await async_worker("task_A", 1.0)
    result2 = await async_worker("task_B", 1.5)
    result3 = await async_worker("task_C", 1.0)

    elapsed = time.perf_counter() - start

    print(f"[SEQUENTIAL] Results: {[result1, result2, result3]}")
    print(f"[SEQUENTIAL] Elapsed time: {elapsed:.2f} seconds")

    return [result1, result2, result3]


async def run_concurrent_with_gather() -> List[str]:
    """
    gather를 이용한 동시 실행 예시

    한국어 설명
    - 여러 코루틴을 동시에 스케줄링
    - 대기 시간이 겹치므로 전체 시간이 줄어드는 경우가 많다.
    """
    print("\n=== Demo 2: Concurrent Async Execution with gather ===")

    start = time.perf_counter()

    results = await asyncio.gather(
        async_worker("task_X", 1.0),
        async_worker("task_Y", 1.5),
        async_worker("task_Z", 1.0),
    )

    elapsed = time.perf_counter() - start

    print(f"[GATHER] Results: {results}")
    print(f"[GATHER] Elapsed time: {elapsed:.2f} seconds")

    return list(results)


# ============================================================
# 2) create_task Basics
# ============================================================

async def small_task(task_id: int) -> str:
    """
    짧은 비동기 작업
    """
    print(f"[TASK] task_id={task_id} started")
    await asyncio.sleep(0.5)
    print(f"[TASK] task_id={task_id} finished")
    return f"result_{task_id}"


async def demo_create_task() -> None:
    """
    create_task() 기초 예시

    한국어 설명
    - create_task()는 코루틴을 즉시 스케줄링하여 Task 객체로 만든다.
    - 이후 await로 결과를 받거나 gather와 함께 사용할 수 있다.
    """
    print("\n=== Demo 3: create_task Basics ===")

    task1 = asyncio.create_task(small_task(1))
    task2 = asyncio.create_task(small_task(2))
    task3 = asyncio.create_task(small_task(3))

    print("[MAIN] Tasks created and scheduled.")

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print("[MAIN] Task results:", [result1, result2, result3])


# ============================================================
# 3) Simulated API Calls
# ============================================================

async def fake_api_call(endpoint: str, delay: float) -> dict:
    """
    API 호출을 흉내 내는 비동기 함수

    한국어 설명
    - 실제 requests 대신 sleep으로 네트워크 대기를 모사
    - 실무에서는 aiohttp 같은 라이브러리와 함께 자주 사용
    """
    print(f"[API] Calling {endpoint} ...")
    await asyncio.sleep(delay)

    response = {
        "endpoint": endpoint,
        "status": 200,
        "data": f"mock_data_for_{endpoint}"
    }

    print(f"[API] Completed {endpoint}")
    return response


async def demo_fake_api_calls() -> None:
    """
    여러 API-like 작업을 비동기로 처리하는 예시
    """
    print("\n=== Demo 4: Simulated API Calls ===")

    start = time.perf_counter()

    responses = await asyncio.gather(
        fake_api_call("/users", 1.0),
        fake_api_call("/orders", 1.5),
        fake_api_call("/products", 0.8),
    )

    elapsed = time.perf_counter() - start

    print("[API] Responses:")
    for response in responses:
        print(response)

    print(f"[API] Total elapsed time: {elapsed:.2f} seconds")


# ============================================================
# 4) Asyncio Mental Model
# ============================================================

def explain_asyncio_concept() -> None:
    """
    asyncio 개념 설명 출력
    """
    print("\n=== Demo 5: Asyncio Mental Model ===")
    print("asyncio는 여러 스레드를 만들지 않아도,")
    print("대기 시간이 있는 작업들을 효율적으로 스케줄링할 수 있다.")
    print()
    print("핵심 아이디어:")
    print("- 작업이 기다리는 동안(event loop에 제어를 넘기는 동안)")
    print("- 다른 작업이 실행될 수 있다.")
    print()
    print("즉:")
    print("time.sleep()  -> 전체 흐름을 멈추게 할 수 있음")
    print("asyncio.sleep() -> 이벤트 루프에 제어를 넘기며 비동기적으로 기다림")


# ============================================================
# 5) Main Async Entry
# ============================================================

async def main() -> None:
    """
    전체 데모 실행
    """
    explain_asyncio_concept()
    await run_sequential()
    await run_concurrent_with_gather()
    await demo_create_task()
    await demo_fake_api_calls()

    print("\n=== Summary ===")
    print("1. async def는 비동기 코루틴을 정의한다.")
    print("2. await는 비동기 작업 완료를 기다리며 이벤트 루프에 제어를 넘긴다.")
    print("3. asyncio.gather()는 여러 코루틴을 동시에 실행하는 데 유용하다.")
    print("4. create_task()는 작업을 명시적으로 스케줄링할 때 유용하다.")
    print("5. asyncio는 대기 시간이 있는 작업에서 특히 강력하다.")


if __name__ == "__main__":
    asyncio.run(main())