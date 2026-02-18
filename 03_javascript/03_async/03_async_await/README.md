## 🧠 Conceptual Positioning

Async/Await is **not a replacement for Promises**.  
It is a **structured abstraction layer** built on top of Promise-based systems.

Async/Await does not change how asynchronous logic works internally —  
it improves how we structure and reason about it.

---

async/await는 Promise를 대체하는 개념이 아니라,  
Promise 기반 코드를 **구조적으로 표현하기 위한 문법 레이어**입니다.

내부 동작을 바꾸는 것이 아니라,  
비동기 로직을 더 명확하게 설계하고 사고할 수 있게 해줍니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain why `async` always returns a Promise
- Use `await` to model sequential async logic clearly
- Centralize error handling with `try/catch/finally`
- Compare sequential vs parallel execution performance
- Choose correct concurrency strategy:
  - `Promise.all()` — fail-fast
  - `Promise.allSettled()` — partial success
  - `Promise.race()` — timeout / race patterns
- Design maintainable async pipelines suitable for real API workflows

---

본 모듈 완료 후 다음을 수행할 수 있습니다:

- async 함수의 반환 구조 설명
- await 기반 순차 흐름 모델링
- try/catch를 활용한 에러 중앙화
- 순차 vs 병렬 실행 성능 비교
- 상황에 맞는 병렬 전략 선택
- 확장 가능한 비동기 설계 구조 구현

---

## 📂 Files & Progress

Each file represents one architectural step toward production-grade async design.

---

### ✅ Day 29 — Async / Await Fundamentals  
`01_async_await_basics.js`

#### 🔎 Core Coverage

- `async` function contract (implicit Promise wrapping)
- Sequential execution modeling with `await`
- Structured error handling via `try/catch/finally`
- Concurrency fundamentals:
  - `await Promise.all([...])`
  - `await Promise.allSettled([...])`
- Timeout pattern using `Promise.race()`
- Fail-fast vs partial-success comparison

#### 🇰🇷 한국어 요약

- async 함수의 Promise 반환 원리
- await 기반 순차 실행 구조화
- try/catch/finally 에러 처리 패턴
- 병렬 실행 전략 비교
- race 기반 timeout 설계
- 실패 전략 선택 기준 이해

---

### ✅ Day 30 — Parallel Await & Concurrency Strategy  
`02_parallel_await.js`

#### 🔎 Core Coverage

- Sequential vs parallel execution benchmarking
- Fail-fast concurrency (`Promise.all`)
- Partial-success concurrency (`Promise.allSettled`)
- Execution time comparison
- Controlled concurrency pattern (worker pool design)
- Production-safe orchestration patterns

#### 🇰🇷 한국어 요약

- 순차 vs 병렬 실행 성능 비교
- fail-fast 전략 이해
- 부분 성공 허용 전략 설계
- 실행 시간 분석
- 동시성 제한 패턴 구현
- 실무형 비동기 오케스트레이션 설계

---

## 🧠 Why Async / Await Matters

Async/Await improves:

- ✅ Readability (linear control flow)
- ✅ Debuggability
- ✅ Error consistency
- ✅ Maintainability
- ✅ Scalability

It enables asynchronous code to be reasoned about  
in a **synchronous mental model**.

---

async/await는 비동기 코드를  
동기 코드처럼 사고할 수 있게 만드는 구조화 도구입니다.

가독성, 유지보수성, 확장성 측면에서  
실무 프로젝트에서 사실상 표준 패턴입니다.

---

## 🔄 Execution Strategy Patterns

### 1️⃣ Sequential Execution (의존성 존재)

```js
const a = await taskA();
const b = await taskB(a);