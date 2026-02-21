# Error Handling (JavaScript Async — Step 4)

This directory covers **production-oriented error handling patterns** for asynchronous JavaScript.
It goes beyond “catch the error” and focuses on **operational reliability**:

- Structured exception handling (`try/catch/finally`)
- Error classification (transient vs fatal)
- Retry strategies (with exponential backoff)
- Designing failure-aware async pipelines

본 디렉토리는 JavaScript 비동기 환경에서의 **실무형 에러 처리 설계**를 다룹니다.  
단순히 “에러를 잡는다” 수준이 아니라, 운영 환경에서 중요한:

- 예외 처리 구조화 (`try/catch/finally`)
- 에러 유형 분류 (일시적 오류 vs 치명적 오류)
- 재시도 전략 설계 (exponential backoff)
- 실패를 고려한 비동기 파이프라인 설계

를 목표로 합니다.

---

## 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain how errors propagate in async flows
- Use `try/catch/finally` to centralize error handling
- Design predictable cleanup logic (`finally`)
- Implement retry for **transient failures** safely
- Use exponential backoff to reduce load during outages
- Avoid unsafe patterns (infinite retry, swallowing errors)

본 모듈 완료 후 다음을 수행할 수 있습니다:

- async 흐름에서 에러 전파 구조 설명
- `try/catch/finally`로 에러 처리를 중앙화
- `finally`로 정리(cleanup) 로직을 안정적으로 보장
- 일시적 오류에 대한 재시도(retry) 전략 구현
- exponential backoff로 장애 시 부하 완화
- 무한 재시도/에러 삼키기 같은 위험 패턴 회피

---

## 📂 Files & Progress

### ✅ Day 32 — Try / Catch / Finally
`01_try_catch_finally.js`

**Core Coverage**
- `try/catch/finally` syntax and contract
- Async error capture (`await` inside `try`)
- Error rethrow vs swallow trade-offs
- Cleanup patterns (close, reset, rollback)
- A consistent error-handling “shape” for real workflows

**한국어 요약**
- try/catch/finally의 동작 원리 정리
- await 기반 비동기 예외를 안전하게 처리
- 에러를 다시 던질지(rethrow) / 내부에서 처리할지 기준
- finally 기반 자원 정리(cleanup) 패턴
- 실전 워크플로우에서 일관된 에러 처리 구조화

---

### ✅ Day 33 — Retry with Exponential Backoff
`02_retry_backoff.js`

**Core Coverage**
- Transient failure modeling (e.g., network / 5xx / timeout)
- Bounded retry (`maxRetries`) to prevent infinite loops
- Exponential backoff: `delay = baseDelay * 2^attempt`
- Failure escalation: retry → final failure throw
- Operational mindset: reducing load during outage windows

**한국어 요약**
- 네트워크/서버 5xx 등 “일시적 실패”를 가정한 구조
- 무한 재시도 방지: `maxRetries`로 상한 설정
- backoff 공식: `baseDelay * 2^attempt`
- 재시도 실패 시 최종 실패로 승격(throw)
- 장애 시점에 서버 부하를 줄이기 위한 운영 설계 관점

> Note (실무 팁): 운영 환경에서는 **jitter(랜덤 지연)** 를 섞어
> 동시에 재시도하는 트래픽 폭주(thundering herd)를 완화합니다.

---

## 🧠 Design Notes (Architecture)

### 1) Error Handling is part of control flow
Errors are not “exceptions to ignore.”  
They are **a control-flow path** that must be designed intentionally.

에러는 “예외적으로 무시할 것”이 아니라,  
의도적으로 설계해야 하는 **하나의 제어 흐름**입니다.

### 2) Retry is only for transient failures
Retry should be applied **only** when failure is likely temporary.
For fatal errors (invalid input, auth failure, logic bugs), retry wastes time and resources.

재시도는 “일시적 오류”에만 적용해야 합니다.  
치명적 오류(권한 실패, 입력 오류, 버그)에 재시도는 자원 낭비입니다.

---

## 🔄 Recommended Flow (실무형 패턴)

```text
Call async operation
    ↓
try/catch: classify error
    ↓
if transient → retry with backoff (bounded)
else → fail fast / surface error
    ↓
finally: cleanup (always)