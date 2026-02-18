# Async/Await (JavaScript Async — Step 3)

This directory covers **async/await**, the modern syntax layer built on top of Promises.

It focuses not only on basic usage, but on **production-grade async control flow**:

- Clear sequential logic (`await`)
- Centralized error handling (`try/catch/finally`)
- Concurrency patterns (`Promise.all`, `allSettled`)
- Operational patterns (timeouts, fail-fast vs partial success)

본 디렉토리는 Promise 위에 구축된 현대적 비동기 문법인  
**async/await**를 다룹니다.

단순 문법 학습이 아니라, 실무에서 필요한:

- 순차 실행 구조화
- 에러 처리 중앙화
- 병렬 실행/부분 성공 전략
- 타임아웃 등 운영 패턴

까지 포함해 **설계 관점(architecture)**으로 정리합니다.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

- Explain what `async` returns (always a Promise)
- Use `await` to express sequential async workflows cleanly
- Handle errors consistently with `try/catch/finally`
- Choose correct concurrency strategy:
  - `Promise.all()` (fail-fast)
  - `Promise.allSettled()` (partial success)
  - `Promise.race()` (timeouts / race patterns)
- Design maintainable async pipelines that scale to real API workflows

---

## 📂 Files & Progress

Each file represents one practical step.

### ✅ Day 29 — Async/Await Fundamentals  
`01_async_await_basics.js`

**Covers**

- `async` function contract (returns Promise)
- `await` for sequential control flow
- `try/catch/finally` error handling patterns
- Concurrency:
  - `await Promise.all([...])`
  - `await Promise.allSettled([...])`
- Timeout pattern using `Promise.race()`
- Fail-fast vs partial-success strategies

**한국어 요약**

- async 함수는 항상 Promise를 반환
- await로 순차 흐름을 구조적으로 표현
- try/catch/finally로 에러 처리를 중앙화
- 병렬 실행(all) / 부분 성공(allSettled) 설계
- Promise.race 기반 timeout 패턴 구현
- 실무 비동기 설계 전략(실패 전략) 학습

---

## 🧠 Why Async/Await Matters

Async/await is not a new async system —  
it is **syntactic structure** over Promises.

It matters because it:

- Makes async code readable like synchronous code
- Reduces nesting and callback-style complexity
- Allows structured error handling
- Improves maintainability for real-world workflows:
  - API calls
  - data fetching pipelines
  - file/network I/O
  - UI state updates

async/await는 Promise를 “대체”하는 것이 아니라,  
Promise 기반 비동기 코드를 **사람이 읽기 좋은 구조로 바꾸는 문법 레이어**입니다.

---

## 🔄 Async Strategy Cheat Sheet

### Sequential (의존성이 있는 작업)
```js
const a = await taskA();
const b = await taskB(a);