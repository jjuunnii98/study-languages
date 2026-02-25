# 🌐 Fetch API — Basic Requests (01_fetch_basic)

This module introduces the **Fetch API** in modern JavaScript,
starting with a production-oriented GET request implementation.

It focuses not only on making requests,
but on building **reliable and safe API interaction patterns**.

---

본 디렉토리는 JavaScript의 **Fetch API 기본 구조**를 다룹니다.

단순히 `fetch(url)`을 호출하는 수준이 아니라,

- HTTP 상태 코드 검증
- 네트워크 오류와 HTTP 오류 구분
- JSON 파싱 안정성 확보
- AbortController 기반 타임아웃 처리
- 재사용 가능한 GET 헬퍼 함수 설계

를 목표로 합니다.

---

# 🎯 Learning Objectives (Day 35)

After completing Day 35, you will be able to:

- Explain how `fetch()` works internally
- Distinguish between network errors and HTTP errors
- Validate `response.ok` correctly
- Parse JSON responses safely
- Implement timeout using `AbortController`
- Build a reusable GET utility function

---

본 학습 완료 후 다음을 수행할 수 있습니다:

- fetch 동작 구조 설명
- 네트워크 오류와 HTTP 오류 구분
- `response.ok`를 통한 상태코드 검증
- 안전한 JSON 파싱 처리
- AbortController 기반 타임아웃 구현
- 재사용 가능한 GET 요청 함수 설계

---

# 📂 Files

## ✅ Day 35 — Fetch GET with Timeout  
`01_fetch_get.js`

### Core Concepts Covered

- Basic GET request using `fetch`
- HTTP status validation (`response.ok`)
- Error throwing for non-2xx responses
- JSON response parsing
- Timeout control using `AbortController`
- Proper cleanup with `finally`

---

# 🧠 Key Design Concepts

## 1️⃣ Fetch Does NOT Reject on HTTP Errors

`fetch()` only rejects on **network failures**.

HTTP errors (404, 500, etc.) must be checked manually:

```javascript
if (!response.ok) {
  throw new Error(`HTTP Error: ${response.status}`);
}