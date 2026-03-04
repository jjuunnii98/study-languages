# 🚦 Rate Limiting (REST API) — Day 43

This document explains **API Rate Limiting**, a critical concept for building
reliable and scalable REST APIs.

Rate limiting controls **how many requests a client can send within a time window**.

본 문서는 REST API에서 중요한 개념인 **Rate Limiting(요청 제한)** 을 설명합니다.

Rate limiting은 **일정 시간 동안 허용되는 API 요청 수를 제한하는 메커니즘**입니다.

---

# 🎯 Why Rate Limiting Exists

APIs use rate limiting to prevent:

- server overload
- abusive traffic
- denial-of-service attacks
- unfair resource usage

API 서버는 다음을 방지하기 위해 rate limit을 사용합니다:

- 서버 과부하
- 악의적 트래픽
- DDoS 공격
- 특정 사용자 독점 사용

---

# 🧠 Basic Concept

Example rule:

100 requests / minute

Meaning:

- A client can send **100 requests**
- within **1 minute**

If the limit is exceeded, the API will reject further requests.

---

# ⚠️ HTTP Status Code

When rate limit is exceeded:

HTTP 429 Too Many Requests

Example response:

{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded"
}

---

# ⏱ Common Rate Limit Strategies

## 1️⃣ Fixed Window

100 requests / minute

단순하지만 **경계 시점에서 트래픽 폭주**가 발생할 수 있음.

Example:

00:00 → 100 requests allowed  
00:01 → reset

---

## 2️⃣ Sliding Window

Requests are calculated in a **rolling time window**.

Example:

Last 60 seconds

장점:

- 더 부드러운 트래픽 제어

---

## 3️⃣ Token Bucket

Clients receive **tokens** to send requests.

Example:

10 tokens / second

If tokens are available → request allowed.

장점:

- burst traffic 허용 가능

---

# 📦 Example Rate Limit Headers

Many APIs include rate information in headers.

Example:

X-RateLimit-Limit: 100  
X-RateLimit-Remaining: 45  
X-RateLimit-Reset: 1672531200

Meaning:

Limit → 최대 요청 수  
Remaining → 남은 요청 수  
Reset → 리셋 시간

---

# 🧑‍💻 Client-Side Handling Strategy

API 클라이언트는 rate limit을 고려해야 한다.

Best practices:

- retry after delay
- exponential backoff
- caching responses
- batching requests

Example strategy:

request → 429 error → wait → retry

---

# 🔁 Retry Strategy Example

Pseudo flow:

request  
↓  
429 Too Many Requests  
↓  
wait (2s)  
↓  
retry  

Advanced strategy:

delay = baseDelay * 2^attempt

이를 **Exponential Backoff** 라고 한다.

---

# 📊 Real API Examples

Many major APIs enforce rate limits.

Examples:

GitHub API → 5000 requests/hour  
Twitter API → endpoint-based limits  
OpenAI API → token + request limits

---

# ⚙️ API Design Perspective

API designers use rate limiting to:

- ensure system stability
- maintain fair access
- protect infrastructure
- control operational cost

---

# 🧠 Developer Perspective

Client developers should:

- avoid unnecessary polling
- use caching
- batch API calls
- respect retry headers

---

# 🚀 Summary

Rate limiting is essential for **stable API ecosystems**.

It protects:

- infrastructure
- system fairness
- service availability

Understanding rate limits is crucial when designing
both **APIs** and **API clients**.

---

# 📌 Related Topics

Next topics in this module:

- API Error Handling
- Retry Logic
- Exponential Backoff
- API Client Architecture