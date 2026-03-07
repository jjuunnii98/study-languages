# 🧾 JSON Handling — 03_json_handling

This directory covers **practical JSON handling patterns** in modern JavaScript.

JSON is the most common data format for API communication,
but real-world API responses are rarely simple.

This module focuses on how to:

- convert between objects and JSON strings
- safely access deeply nested properties
- normalize nested API responses into flat structures
- build safer and more maintainable data-processing code

본 디렉토리는 JavaScript에서의 **실무형 JSON 처리 패턴**을 다룹니다.

JSON은 API 통신에서 가장 많이 사용하는 데이터 형식이지만,  
실제 응답은 단순하지 않고 중첩 구조를 가지는 경우가 많습니다.

이 모듈에서는 다음을 다룹니다:

- 객체 ↔ JSON 문자열 변환
- 중첩 객체 안전 접근
- 중첩 응답 평탄화(normalize / flatten)
- 유지보수 가능한 데이터 처리 구조 설계

---

# 🎯 Learning Objectives

After completing this module, you will be able to:

- Explain the difference between a JavaScript object and a JSON string
- Use `JSON.parse()` and `JSON.stringify()` correctly
- Safely access nested API response data with optional chaining
- Avoid runtime errors caused by missing properties
- Convert nested JSON into flat, analysis-friendly objects
- Build reusable JSON handling utilities for API workflows

본 모듈 완료 후 다음을 수행할 수 있습니다:

- JavaScript 객체와 JSON 문자열의 차이 설명
- `JSON.parse()` / `JSON.stringify()` 정확히 사용
- optional chaining으로 중첩 응답 안전 접근
- 누락된 속성으로 인한 런타임 오류 방지
- 중첩 JSON을 평면 구조로 변환
- API 처리용 재사용 가능한 JSON 유틸 설계

---

# 📂 Files & Progress

---

## ✅ Day 44 — JSON Parse & Stringify  
`01_json_parse_stringify.js`

### Core Coverage

- `JSON.stringify()` for object → JSON string conversion
- `JSON.parse()` for JSON string → object conversion
- Pretty-print formatting with spacing
- Filtering fields during stringify
- Error handling for invalid JSON
- Basic API JSON response handling with `fetch`

### 핵심 개념

JSON 처리의 가장 기본은 다음 두 가지입니다.

- `JSON.stringify()` → 객체를 문자열로 변환
- `JSON.parse()` → 문자열을 객체로 변환

이 과정은 API 요청/응답 처리의 출발점입니다.

### Example

```javascript
const jsonString = JSON.stringify(userObject);
const parsedObject = JSON.parse(apiResponse);
```

---

## ✅ Day 45 — Deep Access & Optional Chaining

02_deep_access_optional_chaining.js

Core Coverage
	•	Deep object access in nested JSON structures
	•	Runtime error risk from missing properties
	•	Safe access using optional chaining (?.)
	•	Default values using nullish coalescing (??)
	•	Safe nested access in arrays and API responses

핵심 개념

실제 API 응답은 보통 중첩 구조입니다.

예:
'''
user.address.geo.lat
'''

하지만 중간 속성이 없으면 오류가 발생할 수 있습니다.

이를 해결하는 핵심이:
	•	?. → optional chaining
	•	?? → nullish coalescing

Example:
'''
const city = user.address?.city ?? "Unknown";
'''

---

## ✅ Day 46 — Normalize & Flatten JSON

03_normalize_flatten.js

Core Coverage
	•	Nested JSON → flat object transformation
	•	Recursive flattening logic
	•	Dot-notation key generation
	•	Array-containing object handling
	•	Normalizing multiple API records
	•	Why flattening matters for UI, CSV, and analytics

핵심 개념

중첩 JSON은 그대로는 다루기 불편한 경우가 많습니다.

예:
'''
user.profile.age
user.address.city
'''

이를 다음처럼 평면 구조로 변환할 수 있습니다:
'''
{
  "user.profile.age": 28,
  "user.address.city": "Seoul"
}
'''

이 구조는:
	•	테이블 렌더링
	•	CSV/Excel export
	•	데이터 분석
	•	UI 바인딩

에 더 적합합니다.

---

## 🧠 Recommended JSON Handling Flow
'''
Raw API Response
    ↓
Check response status
    ↓
Parse JSON safely
    ↓
Access nested fields safely
    ↓
Normalize / flatten if needed
    ↓
Use in UI / analytics / storage
'''

---

## ⚙️ Practical Design Principles

### 1️⃣ Distinguish JSON String vs JavaScript Object

A JSON string is not directly usable like an object.
'''
const obj = JSON.parse(jsonString);
'''

문자열 상태에서는 속성 접근이 불가능하므로
반드시 객체로 변환해야 합니다.

### 2️⃣ Never Assume Nested Fields Always Exist

Real APIs often return incomplete or partially missing fields.
'''
user.address?.geo?.lat
'''

이런 방식으로 접근해야 안전합니다.

### 3️⃣ Flatten When Structure Becomes Hard to Use

Nested JSON is good for transport,
but flat objects are often better for:
	•	table rendering
	•	analytics
	•	export pipelines
	•	form binding

### 4️⃣ Add Error Handling Around Parsing

Invalid JSON throws a SyntaxError.
'''
try {
  const data = JSON.parse(invalidJson);
} catch (error) {
  console.error(error.message);
}
'''

실무에서는 항상 예외 처리와 함께 사용해야 합니다.

---

## 🚀 Current Status

Day 44–46 Completed

This module now demonstrates:
	•	JSON parsing/stringifying basics
	•	safe deep access with optional chaining
	•	normalization/flattening for nested API responses
	•	production-style handling of real-world JSON data

## 🔜 Future Expansion

Possible next topics:
	•	JSON validation
	•	schema-based response checking
	•	API response transformation pipelines
	•	error-safe normalization strategies
	•	versioned API response handling

## 🏁 Summary

This module builds the foundation for safe and maintainable JSON processing in JavaScript.

It demonstrates how to move from:
	•	raw API response strings
	•	to safe object access
	•	to normalized, application-friendly data structures

Understanding JSON handling is essential for building robust API-driven applications.