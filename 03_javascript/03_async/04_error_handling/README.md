# ⚠️ Error Handling (JavaScript Async — Step 4)

This module implements a **production-grade error handling architecture**
for asynchronous JavaScript systems.

It moves beyond basic `catch` usage and focuses on:

- Structured exception handling (`try/catch/finally`)
- Error classification (transient vs fatal)
- Bounded retry strategies
- Exponential backoff
- Custom error modeling
- Failure-aware async pipeline design

---

본 디렉토리는 JavaScript 비동기 환경에서의  
**실무형 에러 처리 아키텍처 설계**를 다룹니다.

단순히 “에러를 잡는다” 수준이 아니라:

- 예외 처리 구조화
- 에러 유형 분류
- 재시도 전략 설계
- 커스텀 에러 모델링
- 운영 환경에서의 안정성 확보

를 목표로 합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain async error propagation mechanics
- Centralize error handling using `try/catch`
- Guarantee cleanup with `finally`
- Implement safe bounded retries
- Apply exponential backoff correctly
- Design custom error classes
- Avoid anti-patterns (infinite retry, swallowed errors)

---

# 📂 Files & Structure

---

## ✅ Day 32 — Try / Catch / Finally  
`01_try_catch_finally.js`

### Covers

- Async error propagation
- `try/catch/finally` execution order
- Rethrow vs swallow trade-offs
- Guaranteed cleanup patterns

### Key Principle

> Errors are part of control flow — design them intentionally.

---

## ✅ Day 33 — Retry with Exponential Backoff  
`02_retry_backoff.js`

### Covers

- Transient failure modeling
- Bounded retry (`maxRetries`)
- Exponential backoff formula:

delay = baseDelay * 2^attempt

- Retry escalation strategy
- Operational load protection

### Production Insight

Retry is not repetition.  
Retry is **controlled recovery strategy**.

---

## ✅ Day 34 — Custom Error Architecture  
`03_custom_error.js`

### Covers

- Base `AppError` class
- Domain-specific subclasses:
  - `ValidationError`
  - `NotFoundError`
  - `NetworkError`
- HTTP status codes
- Retryable flag
- Centralized error handler pattern

### Design Philosophy

Errors are structured objects — not strings.

```javascript
class AppError extends Error {
  constructor(message, statusCode, retryable) {
    super(message);
    this.statusCode = statusCode;
    this.retryable = retryable;
  }
}