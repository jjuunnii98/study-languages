# Fetch Basics (JavaScript API — 01_fetch_basic)

This directory covers **fetch() fundamentals** for calling HTTP APIs in modern JavaScript.  
It goes beyond “just fetching data” and focuses on **production-oriented request/response patterns**:

- HTTP request/response lifecycle
- JSON serialization/deserialization
- Status code validation (`response.ok`)
- Error propagation strategy (don’t swallow errors)
- Timeout / abort control (`AbortController`)
- Headers & querystring patterns
- Safe response parsing (JSON / text / empty-body)

본 디렉토리는 JavaScript의 `fetch()`를 사용해 API를 호출하는 기본을 다룹니다.  
단순 GET 예제를 넘어서 **실무에서 안전하게 동작하는 API 호출 구조**를 목표로 합니다.

---

## 🎯 Learning Objectives

By completing this module, you will be able to:

- Send GET/POST requests using `fetch()`
- Serialize request bodies correctly (`JSON.stringify`)
- Parse responses safely (`response.json()` vs `response.text()`)
- Validate HTTP status codes correctly (`response.ok`)
- Explain why fetch does **not** auto-throw on 4xx/5xx
- Control timeouts using `AbortController`
- Add headers and query parameters safely
- Build reusable API helper functions (client-style abstraction)

본 모듈을 완료하면 다음을 할 수 있습니다:

- `fetch()`로 GET/POST 요청 구현
- 요청 바디를 안전하게 직렬화(`JSON.stringify`)
- 응답을 상황에 맞게 안전 파싱(JSON/텍스트/빈 바디)
- `response.ok` 기반 상태코드 검증
- fetch가 4xx/5xx에서 자동 reject하지 않는 이유 이해
- `AbortController` 기반 timeout 제어
- 헤더/쿼리스트링을 안정적으로 구성
- 재사용 가능한 API 헬퍼 함수(클라이언트 레이어) 설계

---

## 📂 Files & Progress

### ✅ Day 35 — Fetch GET (Basics)
`01_fetch_get.js`

**What it covers**
- Basic GET request with `fetch()`
- JSON parsing (`response.json()`)
- Minimal error handling skeleton
- End-to-end flow: request → parse → use

**한국어 요약**
- fetch GET 호출 흐름
- JSON 응답 파싱
- 최소 에러 처리 골격
- 실전 호출 흐름 구조화

---

### ✅ Day 36 — Fetch POST (Production Pattern)
`02_fetch_post.js`

**What it covers**
- POST request with JSON body (`JSON.stringify`)
- Required headers (`Content-Type: application/json`)
- HTTP status validation (`response.ok`)
- Centralized error propagation (`throw` + caller-side handling)
- Timeout + abort control (`AbortController`)
- Reusable function design (`postJson(payload, timeoutMs)`)

**한국어 요약**
- POST에서 JSON 직렬화/헤더 설정
- `response.ok` 기반 상태코드 검증
- 에러를 삼키지 않고 상위로 전파(throw)
- `AbortController` 기반 timeout 설계
- 재사용 가능한 API 함수화(클라이언트 레이어)

---

### ✅ Day 37 — Headers & Querystring (Request Construction)
`03_headers_querystring.js`

**What it covers**
- Common headers: `Accept`, `Content-Type`, `Authorization` (pattern-level)
- Querystring construction with `URL` / `URLSearchParams`
- Encoding correctness (special chars, spaces)
- Clean GET builder function (`buildUrl(base, params)`)

**한국어 요약**
- 실무에서 자주 쓰는 헤더 패턴 정리
- `URLSearchParams`로 안전한 쿼리스트링 구성
- 인코딩 이슈 회피(특수문자/공백)
- 재사용 가능한 URL 빌더 패턴

---

### ✅ Day 38 — Response Parsing (Safe Parsing Strategy)
`04_response_parsing.js`

**What it covers**
- Safe parsing strategy for:
  - JSON responses
  - Text/HTML responses
  - Empty-body responses (e.g., `204 No Content`)
- `Content-Type` 기반 파싱 분기
- “Parse even on failure” pattern (에러 바디 확보)
- Custom error object pattern (status, url, body 포함)

**한국어 요약**
- JSON/텍스트/빈 바디를 안전하게 처리하는 표준 파서
- `Content-Type` 기반 파싱 분기
- 실패 응답에서도 바디를 파싱해 디버깅 정보 확보
- 실무형 에러 구조(HttpError 등) 설계

---

## 🧠 Key Production Notes (실무 포인트)

### 1) fetch는 4xx/5xx에서 자동으로 실패(reject)하지 않는다
`fetch()`는 네트워크 레벨 실패가 아닌 이상 Promise를 기본적으로 resolve 합니다.  
즉, **404/500도 “성공처럼” 흐를 수 있으므로 `response.ok` 검증이 필수**입니다.

```js
if (!response.ok) {
  throw new Error(`HTTP Error: ${response.status}`);
}
```

### 2) Timeout은 기본 제공되지 않는다 → AbortController로 구현

실무에서는 무한 대기 방지가 필요합니다.

```
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 3000);

try {
  const res = await fetch(url, { signal: controller.signal });
  // ...
} finally {
  clearTimeout(timer);
}
```


### 3) Response parsing은 “항상 안전하게”

현실에서는 응답이 항상 JSON이 아닙니다.
	•	204 No Content (바디 없음)
	•	text/plain / text/html (에러 페이지/메시지)
	•	application/json인데 JSON이 깨져있는 경우

따라서 Content-Type 확인 + 예외 안전 파싱이 중요합니다.


### 4) API 호출은 “함수화”가 유지보수의 시작점

GET/POST 호출을 매번 복붙하면 유지보수가 어려워집니다.
getJson(), postJson(), fetchAndParse() 같은 API 레이어를 만들면:
	•	중복 제거
	•	에러 처리 일관성
	•	timeout/headers 공통화
	•	테스트 용이성

이 확보됩니다.

---

🔄 Recommended Study Order

Fetch GET (Day 35)
    ↓
Fetch POST (Day 36)
    ↓
Headers & Querystring (Day 37)
    ↓
Response Parsing (Day 38)
    ↓
Reusable API Client Abstraction (next)


---

✅ Status

Completed: Day 35–38
This directory now provides a reusable baseline for safe API calls in JavaScript,
covering request construction, error strategy, and robust response parsing.