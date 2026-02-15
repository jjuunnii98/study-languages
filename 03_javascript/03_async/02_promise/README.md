# Promise (JavaScript Async — Step 2)

This directory introduces **JavaScript Promises**,  
the modern foundation of asynchronous control flow.

콜백 기반 비동기 구조의 한계를 해결하기 위해 등장한  
Promise 패턴을 체계적으로 다룹니다.

This module transitions from:
Callback → Promise → async/await

---

## 🎯 Learning Objectives

- Understand Promise state transitions
- Use resolve / reject correctly
- Implement `.then()` chaining
- Handle errors with `.catch()`
- Use `.finally()` for cleanup logic
- Understand error propagation across chains
- Prepare for async/await

---

## 📂 Files & Progress

### ✅ Day 26 — Promise Basics  
`01_promise_basics.js`

Covers:

- Promise constructor mechanics
- Pending → Fulfilled / Rejected states
- `.then()` and `.catch()`
- `.finally()`
- Promise chaining
- Error propagation model

한국어 요약:

- Promise 상태 구조 이해
- resolve / reject 흐름
- then 체이닝
- 중앙집중 에러 처리
- 비동기 제어 흐름 개선

---

## 🧠 What is a Promise?

A Promise is:

> An object representing the eventual completion  
> or failure of an asynchronous operation.

Promise는 비동기 작업의 결과를 표현하는 객체입니다.

It has three states:

- **pending**
- **fulfilled**
- **rejected**

상태는 한 번만 전이되며 되돌릴 수 없습니다.

---

## 🔄 Why Promise Replaced Callback Hell

Callbacks suffer from:

- Deep nesting
- Repeated error handling
- Poor readability
- Difficult flow control

Promises improve:

- Linear chaining
- Centralized error handling
- Composability
- Better maintainability

---

## 📈 Conceptual Async Evolution

```text
Callback
    ↓
Callback Hell
    ↓
Promise
    ↓
async / await