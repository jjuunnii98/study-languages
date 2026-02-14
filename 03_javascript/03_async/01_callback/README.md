# Callback (JavaScript Async — Step 1)

This directory introduces **callback functions**, the foundation of asynchronous programming in JavaScript.

Callbacks are essential for understanding:
- Event loop execution flow
- Asynchronous APIs (`setTimeout`, events, I/O)
- Why Promise and async/await were created

본 디렉토리는 JavaScript 비동기 프로그래밍의 출발점인 **콜백 함수(callback)**를 다룹니다.  
콜백을 이해하면 Event Loop 흐름과 비동기 실행 모델을 체계적으로 이해할 수 있고,  
Promise/async-await로 자연스럽게 확장할 수 있습니다.

---

## 🎯 Learning Objectives

- Understand what a callback function is
- Pass functions as arguments and execute them later
- Simulate asynchronous execution using `setTimeout`
- Learn the error-first callback pattern (Node.js style)
- Recognize the limitations of callbacks (callback hell)
- Prepare for Promise and async/await patterns

---

## 📂 Files & Progress

### ✅ Day 23 — Callback Basics  
**`01_callback_basics.js`**

Covers:
- Callback definition and usage
- Passing named and anonymous callback functions
- `setTimeout` as an async example
- Conceptual event loop flow (Call Stack → Web API → Queue)

한국어 요약:
- 콜백의 기본 개념
- 함수 인자로 함수 전달
- `setTimeout` 기반 비동기 실행 흐름 이해

---

### ✅ Day 24 — Callback Hell  
**`02_callback_hell.js`**

Covers:
- Deeply nested async callbacks (pyramid indentation)
- Error-first callback pattern (`callback(error, result)`)
- Realistic async pipeline example:
  user → orders → payment status → email
- Why callbacks become hard to maintain at scale

한국어 요약:
- 콜백 중첩으로 가독성이 급격히 떨어지는 “콜백 헬” 체감
- 단계별 에러 처리 반복의 비효율성
- Promise/async-await의 필요성을 명확히 이해하는 단계

---

## 🧠 What is a Callback?

A callback is:

> A function passed as an argument to another function,  
> which is executed later (often after an async task finishes).

콜백(callback)은  
다른 함수에 인자로 전달되어 특정 시점에 실행되는 함수입니다.

---

## ⚙️ Event Loop (Conceptual Overview)

Basic async execution flow:

1. Code runs in the Call Stack
2. Async tasks run in Web APIs
3. Completed tasks move to the Task Queue
4. Event Loop pushes queued tasks back to the Call Stack

이 구조를 이해하면 JavaScript의 비동기 실행 흐름을 이해할 수 있습니다.

---

## 🚧 Limitations of Callbacks

Callbacks are powerful but can lead to:

- **Callback hell** (nested indentation)
- Repeated error handling at each step
- Difficult control flow (branching, retries, cancellation)
- Hard-to-test and hard-to-maintain async logic

콜백 구조는 강력하지만,
로직이 길어지면 유지보수와 확장이 어려워집니다.  
이 문제를 해결하기 위해 Promise/async-await가 등장했습니다.

---

## ▶️ How to Run

```bash
node 03_javascript/03_async/01_callback/01_callback_basics.js
node 03_javascript/03_async/01_callback/02_callback_hell.js