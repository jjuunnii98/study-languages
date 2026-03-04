# 🌐 REST API Fundamentals — 02_rest_api

This module implements **core REST API interaction patterns**
using modern JavaScript and the Fetch API.

It focuses on how real-world APIs are **designed, consumed, and structured**.

Topics covered include:

- REST architectural principles
- CRUD endpoint interaction
- Pagination / Sorting / Filtering
- API rate limiting awareness

본 디렉토리는 **REST API의 기본 구조와 실제 API 호출 패턴**을
JavaScript 기반으로 학습하기 위한 모듈입니다.

단순한 fetch 예제를 넘어 다음과 같은 **실무 API 패턴**을 다룹니다.

- REST 구조 이해
- CRUD 요청 구현
- Pagination / Sorting / Filtering
- Rate Limit 대응 개념

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain REST API architecture
- Design resource-oriented endpoints
- Implement CRUD operations using HTTP methods
- Use query parameters for pagination, sorting, and filtering
- Understand API rate limiting concepts
- Build reliable API clients

본 모듈을 완료하면 다음을 수행할 수 있습니다:

- REST API 구조 설명
- Resource 기반 endpoint 설계 이해
- HTTP Method 기반 CRUD 요청 구현
- Query parameter 기반 데이터 제어
- API rate limit 개념 이해
- 안정적인 API 호출 패턴 설계

---

# 📂 Files & Progress

---

## ✅ Day 40 — REST Concepts  
`01_rest_concepts.js`

### Core Coverage

- REST architecture overview
- Resource vs Endpoint concept
- HTTP methods (`GET / POST / PUT / PATCH / DELETE`)
- HTTP status codes
- Fetch example for REST requests

### 핵심 개념

REST는 **Resource 중심 아키텍처**이다.

Example:

'''GET /users
GET /users/1
POST /users
PUT /users/1
DELETE /users/1
'''

---

## ✅ Day 41 — CRUD Endpoints  
`02_crud_endpoints.js`

### Core Coverage

- CRUD operations using fetch
- GET list / GET single
- POST create
- PUT update
- DELETE remove
- Error handling using `response.ok`

### 핵심 개념

CRUD = **Create / Read / Update / Delete**

| Method | Meaning |
|------|------|
| GET | 조회 |
| POST | 생성 |
| PUT | 수정 |
| DELETE | 삭제 |

---

## ✅ Day 42 — Pagination / Sorting / Filtering  
`03_pagination_sort_filter.js`

### Core Coverage

- Query parameter usage
- Pagination implementation
- Sorting logic
- Filtering data
- Combined query strategies

### Example Queries

'''
GET /posts?page=1&limit=10
GET /posts?sort=id&order=desc
GET /posts?userId=1
'''

### 핵심 개념

Query parameters allow **flexible data retrieval**.

Examples:
'''
?page=1
&_limit=10
&_sort=id
&_order=desc
'''

---

## ✅ Day 43 — Rate Limiting  
`04_rate_limit_notes.md`

### Core Coverage

- API request limiting concepts
- HTTP `429 Too Many Requests`
- Rate limiting strategies
- Client retry considerations
- API fairness and infrastructure protection

### 핵심 개념

Rate limiting protects APIs from:

- server overload
- abusive traffic
- unfair resource usage

Example:
'''
00 requests / minute
'''

---

# 🧠 REST API Interaction Flow

'''
Client Application
↓
HTTP Request (Fetch API)
↓
REST API Server
↓
JSON Response
↓
Client Data Processing
'''

---

# ⚙️ Key REST Design Principles

## Resource-Oriented URLs

'''
/users
/users/1
/products
/orders
'''

Avoid verbs:

❌ `/getUsers`  
❌ `/createUser`  

Use nouns:

✅ `/users`  
✅ `/users/1`

---

## HTTP Method Semantics

| Method | Purpose |
|------|------|
| GET | Retrieve resource |
| POST | Create resource |
| PUT | Replace resource |
| PATCH | Partial update |
| DELETE | Remove resource |

---

## Query Parameters

Used for:

- pagination
- filtering
- sorting

Example:

'''/users?page=2&limit=20&sort=name'''

---

# 🚀 Current Status

**REST API Core Completed**

This module demonstrates:

- REST architecture understanding
- CRUD request implementation
- Query parameter usage
- API rate limiting awareness
- production-style Fetch API usage

---

# 🔜 Future Expansion

Possible advanced topics:

- API retry strategies
- Exponential backoff
- API caching
- API client abstraction
- Authentication (JWT / OAuth)
- GraphQL vs REST comparison

---

# 🏁 Summary

This module builds the foundation for **modern API-driven applications**.

Developers learn not only **how to call APIs**,  
but also **how APIs are structured and managed in real-world systems**.