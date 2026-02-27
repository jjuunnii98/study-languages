# Fetch Basics (JavaScript API — 01_fetch_basic)

This directory covers **fetch() fundamentals** for calling APIs in modern JavaScript.

It goes beyond “just fetching data” and focuses on **production-oriented request design patterns**:

- HTTP request / response lifecycle
- JSON serialization / deserialization
- Status code validation (`response.ok`)
- Error propagation strategy
- Timeout & abort control (`AbortController`)
- Header configuration & authentication
- Safe query string construction
- Reusable API helper abstraction

본 디렉토리는 JavaScript의 `fetch()`를 활용한  
**실무형 API 호출 설계 패턴**을 다룹니다.

단순 GET/POST 예제가 아니라,

- 상태 코드 검증
- 에러 전파 구조
- 헤더 설계
- 쿼리스트링 안전 생성
- 타임아웃 제어
- 함수화된 API 레이어 설계

까지 포함한 **운영 관점의 API 호출 구조**를 목표로 합니다.

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Send GET and POST requests correctly
- Serialize and parse JSON safely
- Validate HTTP status codes properly
- Understand why fetch does NOT auto-throw on 4xx/5xx
- Implement timeout logic using `AbortController`
- Build query strings safely using `URLSearchParams`
- Design request headers (Accept / Authorization)
- Structure reusable API client-style helper functions

본 모듈 완료 후 다음을 수행할 수 있습니다:

- `fetch()` 기반 GET/POST 구현
- JSON 직렬화 및 파싱 구조 이해
- HTTP 상태 코드 명시적 검증
- fetch의 resolve 특성(4xx/5xx 자동 reject 아님) 이해
- AbortController 기반 timeout 설계
- URLSearchParams 기반 안전한 query 생성
- Authorization/Accept 헤더 설계
- 재사용 가능한 API 함수화 구조 구현

---

# 📂 Files & Progress

---

## ✅ Day 35 — Fetch GET (Basics)  
`01_fetch_get.js`

### Core Coverage

- Basic GET request
- JSON parsing via `response.json()`
- Minimal error validation pattern
- Request → parse → output flow

### 한국어 요약

- fetch GET 기본 구조
- 응답 JSON 파싱
- 최소 에러 처리
- 요청 흐름 구조 이해

---

## ✅ Day 36 — Fetch POST (Production Pattern)  
`02_fetch_post.js`

### Core Coverage

- POST with JSON body (`JSON.stringify`)
- Required headers (`Content-Type: application/json`)
- HTTP status validation (`response.ok`)
- Centralized error propagation (`throw`)
- Timeout control (`AbortController`)
- Reusable function pattern (`postData(payload, timeoutMs)`)

### 한국어 요약

- POST JSON 직렬화
- 헤더 설정 구조
- response.ok 검증 필수
- 에러를 상위로 전파
- AbortController 기반 timeout 설계
- 재사용 가능한 API 함수화

---

## ✅ Day 37 — Headers & Query String Design  
`03_headers_querystring.js`

### Core Coverage

- Safe query string generation using `URLSearchParams`
- Handling null/undefined query parameters
- Proper header construction (`Accept`, `Authorization`)
- GET request with headers + query parameters
- HTTP error message enrichment (status + body text)
- Clean helper abstraction:
  - `buildQueryString()`
  - `buildHeaders()`
  - `fetchWithQueryAndHeaders()`

### 한국어 요약

- URLSearchParams 기반 안전한 쿼리스트링 생성
- null/undefined 파라미터 필터링
- Authorization(Bearer) 헤더 설계
- Accept 헤더 명시
- 상태코드 + 에러본문 포함 에러 메시지 구성
- API 호출 함수화 구조 완성

---

# 🧠 Critical Production Notes (실무 핵심 포인트)

---

## 1️⃣ fetch는 4xx/5xx에서 자동 실패하지 않는다

`fetch()`는 네트워크 오류가 아닌 이상 Promise를 resolve합니다.

따라서 반드시:

```js
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}