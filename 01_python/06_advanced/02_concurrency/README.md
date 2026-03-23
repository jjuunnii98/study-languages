# Concurrency in Python

This directory covers core concurrency models in Python:

- Threading
- Multiprocessing
- Asyncio

These are essential tools for improving performance and handling multiple tasks efficiently.

---

## 🎯 Learning Objectives

After completing this module, you should be able to:

- understand the difference between threading, multiprocessing, and asyncio
- choose the right concurrency model based on the problem type
- implement basic concurrent workflows
- handle shared state and communication safely
- reason about performance trade-offs in real-world systems

---

## Why Concurrency Matters

Modern applications often need to:

- handle multiple API requests
- process large datasets
- perform background tasks
- respond to users in real time

Concurrency allows programs to:

- improve performance
- utilize system resources efficiently
- handle multiple tasks simultaneously

### 한국어 설명
현대 소프트웨어는 동시에 여러 작업을 처리해야 한다.

예:
- API 여러 개 호출
- 대용량 데이터 처리
- 실시간 서비스 응답

Concurrency는 이런 작업을 효율적으로 처리하기 위한 핵심 기술이다.

---

## Core Models in This Module

| Model | Description | Best For |
|------|------------|----------|
| Threading | Multiple threads within a single process | I/O-bound tasks |
| Multiprocessing | Multiple processes with separate memory | CPU-bound tasks |
| Asyncio | Event-loop-based asynchronous execution | High I/O concurrency |

---

## 🧠 Mental Model

### Threading

```text
One process → multiple threads
Shared memory
```

- lightweight
- shared state (주의 필요)
- good for I/O

### 한국어 설명
하나의 프로세스 안에서 여러 작업 흐름을 동시에 실행하는 방식이다.  
메모리를 공유하기 때문에 빠르지만, 동기화 문제가 발생할 수 있다.

---

### Multiprocessing

```text
Multiple processes → independent memory
```

- true parallelism
- no shared memory by default
- higher overhead

### 한국어 설명
프로세스를 여러 개 띄워 병렬 실행한다.  
CPU 연산에 강하지만, 프로세스 간 통신 비용이 있다.

---

### Asyncio

```text
Single thread → event loop → multiple tasks
```

- cooperative multitasking
- no thread overhead
- excellent for I/O

### 한국어 설명
스레드를 늘리지 않고 이벤트 루프 기반으로 작업을 스케줄링한다.  
대기 시간이 많은 작업에서 매우 효율적이다.

---

## ⚖️ When to Use What

### Use Threading when:
- I/O-heavy workload
- waiting for network, file, or API
- simple concurrency is enough

### Use Multiprocessing when:
- CPU-intensive computation
- heavy numerical processing
- parallel execution is required

### Use Asyncio when:
- many concurrent I/O tasks
- high scalability is needed
- building APIs or async systems

---

## 📂 Directory Structure

| File | Description |
|------|-------------|
| `01_threading_basics.py` | Thread creation, execution, and synchronization basics |
| `02_multiprocessing_basics.py` | Process-based parallelism and inter-process communication |
| `03_asyncio_basics.py` | Coroutine-based asynchronous execution and event loop patterns |

---

## 🔍 Execution Model Comparison

| Feature | Threading | Multiprocessing | Asyncio |
|--------|----------|----------------|--------|
| Parallelism | Limited (GIL) | True parallelism | No (single thread) |
| Memory | Shared | Separate | Shared |
| Complexity | Medium | High | Medium |
| Best Use | I/O-bound | CPU-bound | High I/O concurrency |

---

## ⚠️ Important Considerations

### 1. GIL (Global Interpreter Lock)

- Python threads cannot fully utilize multiple CPU cores
- affects CPU-bound performance

### 한국어 설명
Python의 GIL 때문에 threading은 CPU 작업에서는 제한이 있다.  
그래서 CPU 작업에는 multiprocessing이 더 적합하다.

---

### 2. Shared State

- Threading → shared memory (race condition 가능)
- Multiprocessing → separate memory (Queue 필요)

### 한국어 설명
threading은 변수 공유가 가능하지만 위험하고,  
multiprocessing은 공유가 안 되므로 Queue 같은 도구가 필요하다.

---

### 3. Async Requires Different Thinking

- no blocking calls
- must use async-compatible libraries

### 한국어 설명
asyncio는 기존 코드 방식과 다르기 때문에  
await 기반 흐름을 이해해야 한다.

---

## 🔄 Real-world Mapping

| Scenario | Recommended Approach |
|--------|---------------------|
| API aggregation | Asyncio |
| File downloads | Threading |
| Data processing pipeline | Multiprocessing |
| Web server backend | Asyncio |
| ML feature engineering | Multiprocessing |

---

## 🧪 Recommended Learning Order

```text
1. Threading → 기본 동시성 이해
2. Multiprocessing → 병렬 처리 이해
3. Asyncio → 이벤트 기반 비동기 이해
```

This order builds intuition step-by-step.

---

## 🧱 Practical Insight for AI Engineers

In real-world AI systems:

- Data collection → Asyncio / Threading
- Feature processing → Multiprocessing
- Model inference API → Asyncio
- Batch jobs → Multiprocessing

### 한국어 설명
AI 엔지니어 관점에서:

- 데이터 수집 → 비동기 처리
- 데이터 처리 → 병렬 처리
- API 서비스 → asyncio

이 조합이 가장 많이 사용된다.

---

## Summary

```text
Threading       → I/O concurrency
Multiprocessing → CPU parallelism
Asyncio         → scalable async I/O
```

---

## Final Takeaway

```text
Concurrency is not about doing everything faster.
It is about choosing the right execution model for the workload.
```

### 한국어 핵심 정리

```text
동시성은 "빠르게 만드는 기술"이 아니라,
문제에 맞는 실행 구조를 선택하는 기술이다.
```