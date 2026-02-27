# Fetch Basics (JavaScript API — 01_fetch_basic)

This directory covers **fetch() fundamentals** for calling APIs in modern JavaScript.

It goes beyond “just fetching data” and focuses on **production-oriented patterns**:

- HTTP request/response lifecycle
- JSON serialization/deserialization
- Status code validation (`response.ok`)
- Error propagation and handling strategy
- Timeout / abort control (`AbortController`)
- Reusable API helper function design

본 디렉토리는 JavaScript의 `fetch()`를 사용해 API를 호출하는 기본을 다룹니다.  
단순 GET 예제를 넘어서 **실무에서 안전하게 동작하는 API 호출 구조**를 목표로 합니다.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

- Send GET/POST requests using `fetch()`
- Parse JSON responses safely (`response.json()`)
- Validate HTTP status codes correctly (`response.ok`)
- Understand why fetch does **not** auto-throw on 4xx/5xx
- Implement request timeout using `AbortController`
- Design reusable API client-style helper functions

본 모듈을 완료하면 다음을 할 수 있습니다:

- `fetch()`로 GET/POST 요청을 구현
- JSON 응답을 안정적으로 파싱
- HTTP 상태코드를 올바르게 검증
- fetch가 4xx/5xx에서 자동 reject하지 않는 이유 이해
- AbortController 기반 timeout 구현
- 재사용 가능한 API 헬퍼 함수 설계

---

## 📂 Files & Progress

### ✅ Day 35 — Fetch GET (Basics)
`01_fetch_get.js`

**Covers**
- GET request with `fetch()`
- JSON parsing (`response.json()`)
- Basic error handling pattern
- Response data usage flow (request → parse → output)

**한국어 요약**
- fetch GET 기본 호출 흐름
- 응답 JSON 파싱
- 최소한의 에러 처리 구조
- 실전 호출 흐름 구조화

---

### ✅ Day 36 — Fetch POST (Production Pattern)
`02_fetch_post.js`

**Covers**
- POST request with JSON body (`JSON.stringify`)
- Required headers (`Content-Type: application/json`)
- HTTP status validation (`response.ok`)
- Centralized error propagation (`throw` + caller catch)
- Timeout + abort control (`AbortController`)
- Reusable function design (`postData(payload, timeoutMs)`)

**한국어 요약**
- POST 요청에서 JSON 직렬화/헤더 설정
- fetch의 상태코드 처리 특징(response.ok 직접 검사)
- 에러를 삼키지 않고 상위로 전파하는 구조
- AbortController 기반 timeout 설계
- 재사용 가능한 실무형 API 함수화

---

## 🧠 Important Notes (실무 포인트)

### 1) fetch는 4xx/5xx에서 자동으로 실패하지 않는다
`fetch()`는 네트워크 오류가 아니면 기본적으로 Promise를 resolve 합니다.  
즉, **404/500도 성공처럼 처리될 수 있으므로 `response.ok` 검증이 필수**입니다.

```js
if (!response.ok) {
  throw new Error(`HTTP Error: ${response.status}`);
}
```

### 2) Timeout은 기본 제공되지 않는다 → AbortController로 구현

실무에서는 무한 대기 방지가 필요합니다.

```
const controller = new AbortController();
setTimeout(() => controller.abort(), 3000);
```

### 3) API 호출은 “함수화”가 정답이다

GET/POST 호출을 매번 복붙하면 유지보수가 어려워집니다.
따라서 getData(), postData() 같은 API 레이어 함수 설계가 핵심입니다.

🔄 Recommended Study Order

Fetch GET (Day 35)
   ↓
Fetch POST (Day 36)
   ↓
PUT / PATCH
   ↓
DELETE
   ↓
Reusable API Client abstraction

