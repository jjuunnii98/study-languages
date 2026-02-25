# 🚀 JavaScript Async Architecture — 03_async

This module builds a **complete asynchronous architecture**
in modern JavaScript.

It progresses structurally:

Callback  
→ Promise  
→ async/await  
→ Concurrency Control  
→ Error Handling & Reliability  

This is not syntax study.  
This is **async system design**.

---

본 디렉토리는 JavaScript의 비동기 처리 구조를  
단순 문법 학습이 아니라 **아키텍처 관점**에서 정리합니다.

콜백부터 시작해:

- Promise
- async/await
- 병렬 처리 전략
- 에러 처리 설계
- 재시도 및 운영 안정성

까지 확장합니다.

---

# 🧠 Architectural Evolution

Callback
    ↓
Callback Hell
    ↓
Promise
    ↓
Async / Await
    ↓
Concurrency Control
    ↓
Retry / Backoff
    ↓
Custom Error Architecture


이 흐름은 단순 문법 진화가 아니라  
**제어 흐름 안정화 과정**입니다.

---

# 📂 Module Structure

---

## 01_callback

### Covers

- Callback basics
- Nested callback structure
- Callback Hell
- Transition to Promise

### 핵심 개념

> 콜백은 제어 흐름을 분산시키며  
> 구조적 복잡성을 증가시킨다.

---

## 02_promise

### Covers

- Promise state lifecycle
- `.then()` chaining
- Error propagation
- Promise.all / race / allSettled
- Sequential async pipelines

### 핵심 개념

> Promise는 비동기 상태를 객체로 모델링한다.

---

## 03_async_await

### Covers

- async function contract (always returns Promise)
- await sequential modeling
- try/catch integration
- Parallel execution
- Timeout patterns

### 핵심 개념

> async/await는 Promise 위에 구축된  
> 구조적 표현 레이어다.

---

## 04_error_handling

### Covers

- try/catch/finally
- Bounded retry
- Exponential backoff
- Custom error classes
- Centralized error handling

### 핵심 개념

> 에러는 예외가 아니라  
> 설계해야 하는 실행 경로다.

---

# 🔄 Concurrency Strategy Matrix

| Strategy | Use Case | Behavior |
|-----------|-----------|------------|
| Sequential await | Dependency exists | Ordered execution |
| Promise.all | All must succeed | Fail-fast |
| Promise.allSettled | Partial success allowed | Wait-all |
| Promise.race | Timeout / first response | First resolution |
| Retry + Backoff | Transient failure | Controlled recovery |

---

# ⚙️ Operational Mindset

Async design must consider:

- Error classification
- Retry safety
- Backoff strategy
- Load protection
- Cleanup guarantees
- Structured logging
- Deterministic control flow

비동기 설계는 단순 기능 구현이 아니라  
**운영 안정성 설계**입니다.

---

# 🎯 What This Module Demonstrates

- Structured async control flow
- Error-aware system design
- Retry logic modeling
- Custom error classification
- Production-grade async patterns

---

# 🚀 Current Status

Async architecture completed through:

- Callback
- Promise
- Async/Await
- Concurrency patterns
- Retry with exponential backoff
- Custom error modeling

This module forms a foundation for:

- Backend API development
- Microservice reliability
- Event-driven systems
- Production-grade async workflows