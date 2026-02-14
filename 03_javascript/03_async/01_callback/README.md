# Callback (JavaScript Async — Step 1)

This directory introduces **callback-based asynchronous programming**
and demonstrates the transition from callbacks to Promises.

콜백 기반 비동기 프로그래밍을 이해하고,  
콜백 헬을 거쳐 Promise 및 async/await로 발전하는 과정을 다룹니다.

This module represents the first major step
in mastering JavaScript asynchronous design.

---

## 🎯 Learning Objectives

- Understand what a callback function is
- Simulate asynchronous execution
- Learn the error-first callback pattern (Node.js style)
- Identify the limitations of nested callbacks
- Refactor callback hell into Promise-based logic
- Prepare for async/await

---

## 📂 Files & Progress

### ✅ Day 23 — Callback Basics  
`01_callback_basics.js`

- Callback definition
- Function as argument
- `setTimeout` example
- Event Loop conceptual model

---

### ✅ Day 24 — Callback Hell  
`02_callback_hell.js`

- Nested async callbacks
- Error-first callback pattern
- Multi-step async pipeline
- Structural readability issues

---

### ✅ Day 25 — Callback → Promise Refactor  
`03_callback_to_promise.js`

- Promisifying callback-based functions
- Promise chaining
- async/await implementation
- Centralized error handling

---

## 🔄 Async Evolution (Conceptual Model)

The evolution of asynchronous patterns in JavaScript:

```text
Callback
    ↓
Callback Hell
    ↓
Promise
    ↓
async / await