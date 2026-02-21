# Error Handling (JavaScript Async — Step 4)

====================================================================

This module introduces **structured error handling architecture**
in modern JavaScript systems.

It moves beyond simple syntax usage and focuses on:

- Error propagation models
- try / catch / finally design
- Async/await rejection handling
- Layered error responsibility
- Rethrow (error forwarding) patterns
- Production-oriented stability design

본 모듈은 JavaScript에서의 **구조적 에러 처리 설계(Architecture)**를 다룹니다.

단순 문법 설명이 아니라,
실무에서 필요한:

- 에러 전파 흐름 이해
- async/await 환경에서의 reject 처리
- 계층적 책임 분리
- 재던지기(rethrow) 패턴
- finally 실행 보장 특성

을 설계 관점에서 정리합니다.

====================================================================


## 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain synchronous error vs Promise rejection
- Use try/catch/finally correctly in async workflows
- Understand how await transforms rejection into catchable errors
- Design layered error handling (Service → Controller)
- Implement rethrow patterns safely
- Avoid silent failures and swallowed errors

본 모듈 완료 후 다음을 수행할 수 있습니다:

- 동기 에러와 Promise reject의 차이 설명
- async/await에서 try/catch 정확히 활용
- reject → catch 흐름 이해
- 계층적 에러 책임 분리 설계
- 재던지기 패턴 구현
- 조용히 사라지는 에러 방지


====================================================================


## 📂 Files & Progress

--------------------------------------------------------------------

### ✅ Day 32 — try / catch / finally
`01_try_catch_finally.js`

--------------------------------------------------------------------

### Core Coverage

- Synchronous try/catch fundamentals
- finally execution guarantee
- Async/await rejection handling
- Promise error propagation flow
- Rethrow pattern
- Layered architecture example (Service → Controller)

--------------------------------------------------------------------

### 한국어 요약

- 동기 코드 에러 처리 구조
- finally 블록 실행 보장
- async/await reject 처리 방식
- 에러 계층 전달 구조
- 실무형 서비스/컨트롤러 패턴


====================================================================


## 🧠 Why Error Handling Matters

Error handling is not about “catching errors.”

It is about:

- Defining responsibility boundaries
- Preserving observability
- Maintaining system stability
- Preventing inconsistent states
- Designing predictable failure behavior

에러 처리는 단순히 잡는 것이 아니라,

“어디에서 책임지고 어떻게 복구할 것인가”를 설계하는 문제입니다.

잘못 설계된 에러 처리는 다음을 유발합니다:

- Silent failures
- Unhandled Promise rejections
- Debugging difficulty
- System instability


====================================================================


## 🔄 Error Flow Model

### 1️⃣ Synchronous Flow

throw → catch → finally


### 2️⃣ Async / Await Flow

Promise.reject()
    ↓
await
    ↓
catch
    ↓
finally


====================================================================


## 🏗 Layered Error Architecture

Controller
    ↓
Service
    ↓
Repository / API


✔ 하위 계층:
- 로그 기록
- 필요 시 rethrow

✔ 상위 계층:
- 최종 사용자 응답 처리
- 에러 메시지 가공
- HTTP 상태 코드 결정

이 구조는 Separation of Concerns의 핵심입니다.


====================================================================


## 🧩 Production Best Practices

- Never swallow errors silently
- Always log contextual information
- Rethrow when responsibility belongs to upper layer
- Use custom Error classes for domain-level control
- Handle global unhandled rejections
- Avoid mixing business logic with error formatting logic


====================================================================


## 🚀 Async Evolution Context

Callback
    ↓
Promise
    ↓
async / await
    ↓
Structured Error Handling


이 단계는 Async 설계의 안정화 단계입니다.

비동기 코드를 “동작하는 코드”에서
“운영 가능한 코드”로 전환하는 레이어입니다.


====================================================================


## 📌 Status

Active Development — Day 32 Completed

This module finalizes the async architecture layer
by introducing structured error control.


====================================================================