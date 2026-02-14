# Callback (JavaScript Async — Step 1)

This directory introduces **callback functions**,  
the foundation of asynchronous programming in JavaScript.

콜백 함수는 JavaScript 비동기 프로그래밍의 출발점이며,  
이후 Promise와 async/await를 이해하기 위한 필수 개념입니다.

---

## 🎯 Learning Objectives

- Understand what a callback function is
- Learn how functions can be passed and executed later
- Simulate asynchronous behavior using `setTimeout`
- Understand the basic flow of the Event Loop
- Prepare for Promise and async/await patterns

---

## 📂 File Structure & Progress

### ✅ Day 23 — Callback Basics  
**`01_callback_basics.js`**

This file covers:

- What a callback function is
- Passing functions as arguments
- Anonymous callback functions
- Simulating async execution with `setTimeout`
- Basic understanding of Event Loop flow

---

## 🧠 What is a Callback?

A callback is:

> A function passed as an argument to another function,  
> which is executed later.

콜백(callback)은  
다른 함수의 인자로 전달되어  
특정 시점에 실행되는 함수입니다.

---

## 🔄 Why Callbacks Matter

JavaScript is single-threaded.

비동기 처리를 위해  
JavaScript는 콜백 기반 구조를 사용합니다.

Common use cases:

- setTimeout / setInterval
- Event listeners
- API requests
- File handling (Node.js)

---

## ⚙️ Event Loop (Conceptual Overview)

Basic async execution flow:

1. Code runs in Call Stack
2. Async task moves to Web API
3. When finished → moves to Event Queue
4. Event Loop pushes it back to Call Stack

이 구조를 이해하면  
JavaScript의 비동기 실행 흐름을 이해할 수 있습니다.

---

## 🚧 Limitations of Callbacks

While callbacks are powerful, they can lead to:

- Nested callbacks (Callback Hell)
- Hard-to-read code
- Error handling complexity

이러한 한계를 해결하기 위해  
Promise와 async/await가 등장합니다.

---

## 📌 Summary

- Callback = function passed into another function
- Used for asynchronous execution
- Fundamental concept for JS async model
- Bridge toward Promise and async/await

---

## 🔜 Next Steps

- Callback Hell (Nested callbacks)
- Promise basics
- async / await
- Error handling in async flow

This directory forms the first step  
in mastering JavaScript asynchronous programming.